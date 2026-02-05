# Problem / Context

Defining the architectural style for the LLM Observability Quantum.

# Objectives

- Maximize observability
- Handle concurrency
- High configurability

# Alternatives

- Monolithic
- Microservices
- Event-driven
- Service-Oriented

# Consequences

| Alternative     | Observability | Concurrency | Configurability |
| --------------- | ------------- | ----------- | --------------- |
| Monolithic      | Low           | Low         | Low             |
| Microservices   | High          | High        | High            |
| Event-driven    | High          | High        | Medium          |
| Service-Oriented| Medium        | Medium      | Medium          |

# Tradeoffs

- Monolithic - Low observability, concurrency, and configurability.
- Microservices - High observability, concurrency, and configurability, but can introduce complexity in management.
- Event-driven - High observability and concurrency, but configurability can be less straightforward than microservices.
- Service-Oriented - Moderate support for observability, concurrency, and configurability.

# Decision

Use a Microservices architectural style for the LLM Observability Quantum.

# Status

Accepted
