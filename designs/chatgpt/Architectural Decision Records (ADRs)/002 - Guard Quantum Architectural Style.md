# Problem / Context

Defining the architectural style for the Guard Quantum, which is responsible for the system's security layer to safeguard the LLMs from generating or responding to harmful prompt.

# Objectives

- Prioritize security
- Handle high concurrency
- Allow for easy configurability

# Alternatives

- Layered Architecture
- Microservices
- Event-driven

# Consequences

| Alternative          | Security | High Concurrency | Easy Configurability |
| -------------------- | -------- | ---------------- | -------------------- |
| Layered Architecture | High     | Low              | Medium               |
| Microservices        | Medium   | High             | High                 |
| Event-driven         | High     | High             | High                 |

# Tradeoffs

- Layered Architecture - Provides good security, but can be a bottleneck for concurrency and is not as easily configurable as other options.
- Microservices - Offers high concurrency and configurability, but can introduce security complexities at the service boundaries.
- Event-driven - Excels at handling high concurrency and provides a flexible, configurable security model by reacting to events.

# Decision

Use an Event-driven architectural style for the Guard Quantum.

# Status

Accepted
