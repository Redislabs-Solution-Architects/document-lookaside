# Example of Redis Lookaside Cache with MongoDB

## Summary
API server and client implementation of an application using MongoDB for document storage and Redis for lookaside caching.
## Architecture
### High Level
![High-level Architecture](https://docs.google.com/drawings/d/e/2PACX-1vTRrISLLxRwdTBJA1ddQyPRFlcgMYn-0xSWSuJSRVNR6uzRllbpcaOiw9TH2TKenztWhMkaOAv-9xMH/pub?w=663&amp;h=380 "High Level Architecture")
### Detailed
![Detailed Architecture](https://docs.google.com/drawings/d/e/2PACX-1vSTAmEz0i7cunUaM3Rxw3qQVVBOpGM_8RvgHEEa7haveGm-p5ZPVEkdEntNOGF9kslYuiZljSXyq-ug/pub?w=830&h=290 "Detailed Architecture")
## Features
- Implements a simple conjunctive search on MongoDB and Redis.
- Utilizes RedisJSON for document storage and RediSearch for indexing.
- Though not designed to be a benchmarking app, it does keep track of fetch latencies associated with cache hits and misses.
## Prerequisites
- Docker
- Python
## Installation
1. Clone this repo.
2. Go to document-lookaside folder.
```bash
cd document-lookaside
```
3. Install Python requirements (either in a virtual env or global)
```bash
pip install -r requirements.txt
```
4. Build and start docker containers
```bash
docker compose up
```
5. To access the API via browser:
```bash
http://localhost:8000/cancellations/airports/ATL/2003/6

http://localhost:8000/metrics
```
6. To execute the test client:
```bash
python3 ./tests/test.py
```