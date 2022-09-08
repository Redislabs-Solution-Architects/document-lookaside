from pydantic import BaseModel

class MetricsModel(BaseModel):
    cache_hits: int = 0
    cache_misses: int = 0
    ave_cache_latency: float = 0.0
    ave_db_latency: float = 0.0

    def incr_hits(self, duration: float):
        self.cache_hits += 1
        self.ave_cache_latency = round(self.ave_cache_latency +
                (duration-self.ave_cache_latency)/self.cache_hits, 3)
        
    def incr_misses(self, duration: float):
        self.cache_misses += 1
        self.ave_db_latency = round(self.ave_db_latency +
            (duration-self.ave_db_latency)/self.cache_misses, 3)
