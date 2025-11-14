# Problem / Context

Positioning the rate limiter system in a distributed environment.

# Objectives

- all client requests must go through rate limiter
- rate limits apply to all requests irrespecive of which server pod is handling the request
- when rate limiter is unavailable, application must still be accessible
- rate limiter should not add latency
- rate limiter should be independently deployable

# Alternatives

- place rate limiter at client
- place rate limiter within load balancer
- place rate limiter before load balancer
- place rate limiter within server pods

# Consequences

| Alternative          | All requests through rate limiter | Limits irrespective of server pod | Availability | Latency | Independently deployable |
| -------------------- | --------------------------------- | --------------------------------- | ------------ | ------- | ------------------------ |
| client               | yes                               | yes                               | medium       | low     | no                       |
| within load balancer | yes                               | yes                               | low          | low     | no                       |
| before load balancer | yes                               | yes                               | high         | low     | yes                      |
| within server pods   | yes                               | no                                | high         | low     | no                       |

# Tradeoffs

- client - low latency, but not independently deployable
- within load balancer - low latency, but not independently deployable and availability is dependent on load balancer
- before load balancer - low latency, independently deployable, high availability
- within server pods - limits are not shared across server pods

# Decision

Place rate limiter before load balancer.

# Status

ACCEPTED
