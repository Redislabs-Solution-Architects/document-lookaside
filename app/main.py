from redis import asyncio as aioredis
from redis.commands.search.field import TextField, NumericField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from json import load, loads
from decouple import config
from metrics_model import MetricsModel
from time import perf_counter_ns
from aioredlock import Aioredlock

app = FastAPI()
rdb = aioredis.from_url(config('REDIS_URL'))
lock_mgr = Aioredlock([config('REDIS_URL')]) 
mdb = AsyncIOMotorClient(config('MONGO_URL'))
metrics = MetricsModel()

async def time_func(func, *args):
    """Execute a function and measure its execution time.
    """
    t1 = perf_counter_ns()
    result = await func(*args)
    t2 = perf_counter_ns()
    duration = round((t2 - t1) / 1000000, 3)
    return result, duration

@app.on_event('startup')
async def startup_event():
    #mongo startup
    """Reset the db to an empty state and then load data from file
    """
    col = mdb.airlines.delays
    col.drop()  
    with open('data.json') as json_file:
        data = load(json_file)
    await col.insert_many(data)
    await col.create_index([('airport.code', 1),('time.year', 1),('time.month', 1)])
    
    #redis startup
    """Empty cache and rebuild index.
    """
    await rdb.flushdb()
    idx_def = IndexDefinition(index_type=IndexType.JSON, prefix=['delayStat:'])
    schema = (TextField('$.airport.code', as_name='airport', sortable=True),
                NumericField('$.time.year', as_name='year', sortable=True),
                NumericField('$.time.month', as_name='month', sortable=True))
    await rdb.ft('idx').create_index(schema, definition=idx_def)

@app.on_event('shutdown')
async def shutdown_event():
    mdb.close()
    await rdb.quit()

@app.get('/cancellations/airports/{airport}/{year}/{month}', 
    response_description='Flight cancellation totals for an airport in a given month, year')
async def get_cancellations(airport: str, year: int, month: int):
    try:
        result, duration = await time_func(rdb.ft('idx').search,
                Query(f"(@airport:{airport}) (@year:[{year} {year}]) (@month:[{month} {month}])"))

        if len(result.docs) > 0:  # cache hit
            jsonval = loads(result.docs[0].json)
            metrics.incr_hits(duration)
            return {"result": jsonval['statistics']['flights']['canceled']}
        else:  # cache miss
            col = mdb.airlines.delays
            lock = await lock_mgr.lock(f"lock:{airport}:{year}:{month}")  #fine-grained, distributed lock
            result, duration = await time_func(col.find_one, 
                { "airport.code": airport,
                    "time.year": {"$eq": year},
                    "time.month": {"$eq": month}
            })
            metrics.incr_misses(duration)
            if result:
                id = result.pop('_id')  # this field can't be serialized and needs to be removed
                await rdb.json().set(f"delayStat:{id}", '$', result)  #add val to cache and set TTL to 1 hour
                await rdb.expire(f"delayStat:{id}", 3600)
                await lock_mgr.unlock(lock)
                return {"result": result['statistics']['flights']['canceled']}
            else: # not found in cache or db
                await lock_mgr.unlock(lock)
                raise HTTPException(status_code=404, detail=f"Data not found for {airport} {year} {month}")
    except Exception as err:
        if type(err) == HTTPException:
            raise err
        else:
            raise HTTPException(status_code=400, detail=str(err))

@app.get('/metrics', response_model=MetricsModel)
def get_metrics():
    return metrics

