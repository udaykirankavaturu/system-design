# Problem / Context

The rate limiter needs to handle a large number of requests and store a large number of counters. A single instance may not be able to handle the load and store all the data. We need a way to distribute the load and data across multiple nodes.

# Objectives

- Distribute the request load across multiple rate limiter instances.
- Distribute the counter data across multiple data stores.
- Ensure high availability and fault tolerance.
- Minimize cross-shard communication.

# Alternatives

1.  **Sharding by User ID:** Assign users to shards based on their user ID. For example, `shard_id = hash(user_id) % num_shards`.
2.  **Sharding by Key:** The key to be rate-limited (e.g., IP address, API key) is hashed to a shard.
3.  **Geo-based sharding:** Shard based on the user's geographical location.

# Consequences

| Alternative         | Distribute request load | Distribute counter data | High availability | Minimize cross-shard communication |
| ------------------- | ----------------------- | ----------------------- | ----------------- | ---------------------------------- |
| Sharding by User ID | Medium                  | Medium                  | High              | Low                                |
| Sharding by Key     | High                    | High                    | High              | Low                                |
| Geo-based sharding  | Low                     | Low                     | Medium            | High                               |

# Tradeoffs

- Sharding by User ID is simple to implement but can lead to hotspots.
- Sharding by Key is more effective at distributing load but can still have hotspots.
- Geo-based sharding is good for latency but can lead to uneven load distribution.

# Decision

We will use a combination of sharding by key and consistent hashing. Consistent hashing will help in distributing the keys evenly across the shards and also minimize re-hashing when shards are added or removed.

# Status

Accepted
