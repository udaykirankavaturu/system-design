# ADR03: Choosing the Memory Store

# Status

Proposed

# Problem / Context

Choosing a memory store for the rate limiter.

# Objectives

- Low Latency
- Scalable
- High Availability
- Automatic Data Eviction

# Alternatives

- Redis
- Memcached
- In-process Memory

# Consequences

| Alternative       | Low Latency | Scalable | High Availability | Automatic Data Eviction |
| ----------------- | ----------- | -------- | ----------------- | ----------------------- |
| Redis             | High        | High     | High              | Yes                     |
| Memcached         | High        | High     | Medium            | Yes                     |
| In-process Memory | Very High   | Low      | Low               | No                      |

# Tradeoffs

- **Redis**: High performance and feature-rich, but can be a single point of failure if not clustered.
- **Memcached**: Very fast for simple operations, but less feature-rich than Redis.
- **In-process Memory**: Fastest option, but not scalable or highly available.

# Decision

Use **Redis** as the memory store.

# Status

Proposed