# Problem / Context

Defining the architectural style for the LLM Quantum.

# Objectives

- High concurrency
- High configurability
- Scalability

# Alternatives

- Monolithic
- Microservices
- Event-driven
- Service-Oriented

# Consequences

| Alternative     | High Concurrency | High Configurability | Scalability |
| --------------- | ---------------- | -------------------- | ----------- |
| Monolithic      | Low              | Low                  | Low         |
| Microservices   | High             | Medium               | High        |
| Event-driven    | High             | High                 | High        |
| Service-Oriented| Medium           | Medium               | Medium      |

# Tradeoffs

- Monolithic - Low concurrency, configurability, and scalability.
- Microservices - High concurrency and scalability, but configurability can be complex to manage across services.
- Event-driven - High concurrency, configurability, and scalability are primary strengths.
- Service-Oriented - Moderate support for concurrency, configurability, and scalability.

# Decision

Use an Event-driven architectural style for the LLM Quantum.

# Status

Accepted
