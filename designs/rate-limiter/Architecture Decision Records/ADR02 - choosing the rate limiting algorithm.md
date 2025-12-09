# ADR02: Choosing the Rate Limiting Algorithm

# Status

Proposed

# Problem / Context

Choosing a rate limiting algorithm to protect the system from abuse and overload.

# Objectives

- Accurate
- Memory-Efficient
- Low Latency
- Scalable
- Flexible

# Alternatives

- Token Bucket
- Leaky Bucket
- Fixed Window Counter
- Sliding Window Log
- Sliding Window Counter

# Consequences

| Alternative            | Accurate | Memory-Efficient | Low Latency | Scalable | Flexible |
| ---------------------- | -------- | ---------------- | ----------- | -------- | -------- |
| Token Bucket           | High     | High             | Low         | High     | High     |
| Leaky Bucket           | High     | High             | Low         | High     | Low      |
| Fixed Window Counter   | Low      | High             | Low         | High     | Low      |
| Sliding Window Log     | High     | Low              | Low         | High     | High     |
| Sliding Window Counter | Medium   | Medium           | Low         | High     | High     |

# Tradeoffs

- **Token Bucket**: Flexible and accurate, but can be complex to implement.
- **Leaky Bucket**: Smooths out traffic, but not flexible for bursts.
- **Fixed Window Counter**: Simple, but can be inaccurate at window edges (overlapping windows).
- **Sliding Window Log**: Very accurate, but high memory usage.
- **Sliding Window Counter**: Good balance of accuracy and memory usage, but more complex than Fixed Window.

# Decision

Use the **Sliding Window Counter** algorithm.

# Status

Accepted

# Reference Links

[Byte Byte Go](https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter)
[Arpit Bhayani](https://arpitbhayani.me/blogs/sliding-window-ratelimiter/)
