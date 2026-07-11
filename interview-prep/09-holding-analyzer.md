# Holding Analyzer


09 — Holding Analyzer (Redis caching flagship)

| Repo: + Stack: Plotly Dash, Redis, AWS S3, Pandas, EKS Your role:

Built the dashboard and the Redis caching layer —

Snapshot

“A Plotly Dash app for analysing holdings, backed by Redis caching of $3

-hosted reference data. The dashboard used to fetch data from $3 on every page load — around 3 seconds each time. | added cache}
daily expiry, cutting retrieval from ~3s to ~0.5s and eliminating redundant $3 calls." il 7

| This is the “reduced latency 3s0.5s" bullet on your resume. Know it cold.

STAR story — “Kill the 3-second page load" : i

Situation.

The Holding Analyzer Dash app loaded company reference/holdings data from S3.on every page load. That's ~3 seconds of latency per load, repeated for identical data, hammering S3 with redundant

Task. Make the dashboard load fast and stop re-fetching data that changes only once ade é " q a a) »

Introduced a Redis cache (RedisCache class) using a connection pool (shared — ona|

pooled connection, not a new connection per call).
Cached the S3-derived DataFrames under stable keys; i

on load the app checks R dis first ind onl falls back to S3 on a miss.
invalidates right before fresh data lands. - . i

* Made caching toggleable via a USE_REDIS_ CACHE flag so it can be disabled ae debugging, a : ; eet We

\ % Ri =
Result. Data retrieval dropped from ~3s to ~0.5s (6x faster page loads) and redundant $3 teicheson every page load were eliminated — less S3 cost/traffic and a far snappier UX.

the next day, because the upstream data refreshes daily — so the cache is warm all day and automatically


Technical deep-dive & why

* Why Redis (not in-process memory)? Dash runs multiple workers/pods on EKS. An in-process dict isn't shared ac
worker/pod. i


Toss them, so each worker would still hit S3, Redis is a shared cache — one warm copy

Why a connection pool? Opening a TCP connection to Redis Per request adds latency and exhausts connections under load. A pool
Why expireat 10am Pacific next day (not a fixed TTL like 1 hour)? The cache should invalidate aligned to when the data act:
data after refresh or needlessly re-fetch mid-day. Expiring just before the daily refresh gives maximum hit-rate and freshness.

Why a feature flag? When diagnosing a data issue you need to bypass the cache and read S3 directly. USE_REDIS_CACHE=fallse) does that without a code change.

Freuses connections — this is part of why it's fast and stable.
tually changes, not on an arbitrary clock. A blind 1-hour TT

Code samples (real, extracted from the repo)

Shared, pooled Redis with expiry aligned to the daily data refresh (app/redis cache. py. abridged)

class RedisCache:

pool = redis.ConnectionPool(host=REDIS_HOST, port=REDIS_ PORT, db=0)

# reuse connections
r = redis.Redis(connection_pool=pool)

# shared across pods

def setRedisCache(self, key, values):
now = datetime.datetime.today() + datetime.timedelta(days=1)
# expire at 10:00 US/Pacific TOMORROW — right before the next early refresh lands
expire_at = datetime.datetime( 2

int(now.strftime("%Y")), int(now.strftime("%m")), int(now.strftime("%d")),
10, 0, 0,

) -astimezone(timezone("US/Pacific") )
self.r.set(key, values)
self.r.expireat(key, expire_at) # time—aligned invalidation
def deleteFromRedisCache(self, key):
if self.r.exists(key):
self.r.delete(key)

# explicit manual bust

| Talking point the win isn't set/get — it's expireat aligned to when the data changes plus a connection pool so hits skip both the S3 round-trip and the TCP-connection cost.

Likely follow-up Q&A ee

Q: How exactly did you measure 3s — 0.5s? A: Observed page-load/data-fetch timing before and after — the S3 read path was ~3s; the Redis hit path is ~0.5s. Be honest that it's an observed/approximate figure from load
timing, not a formal benchmark.

Q: What's your cache invalidation strategy — the hard part of caching? A: Time-based, aligned to the data’s daily refresh: keys expireat 10am Pacific the following day. | also have an explicit
deleteFromRedisCache(key) for manual busting. Because the source is append/replace-daily, time-aligned expiry is correct and simple — no complex event-based invalidation needed.

Q: What if Redis is down? A: Treat it as a cache miss and fall back to S3 — the app still works, just slower. The flag also lets us disable Redis entirely. (A hardening step: wrap Redis calls so a connection error degrades to S3
rather than erroring.)

Q: Cache stampede — what if many users hit a cold key at 10am? A: With daily data | can pre-warm the cache right after the upstream refresh (a scheduled load), so the first user never faces a cold miss. Otherwise a short
lock / single-flight around the S3 fetch prevents every worker refetching simultaneously.

Q Why cache the DataFrame and not just the S3 object? A: The expensive part is the $3 round-trip plus parse; storing the ready-to-use serialized frame means a hit skips both the network and the parsing.

