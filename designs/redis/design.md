# System design for 'redis'

Design a distributed key value store such as Redis, Memcached.

# Functional Requirements

- put(key, value) - insert 'value' associated with 'key'
- get(key) - get 'value' associated with 'key'

# Non Functional Requirements

- Data size - max 10 KB per key-value pair
- Ability to store big data
- High availability - The system responds quickly, even during failures
- High scalability - The system can be scaled up to support large dataset
- Automatic scaling: The addition/deletion of servers should be automatic based on traffic.
- Tunable consistency.
- Low latency.

# Actors Actions

```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    A[Server] -->|"put(1,'football')"| B(Redis Node)
```

```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    A[Server] -->|"get(1)"| B(Redis Node)
    B(Redis Node) -->|"football"| A[Server]
```

# Event Storming

```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    C([Event: Key Added or Updated])
    A[Server] -->|"put(1,'football')"| B(Redis Node)

    style C fill:#cce5ff,stroke:#004085,stroke-width:2px,color:#000
```

```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    C([Event: Key Read])
    A[Server] -->|"get(1)"| B(Redis Node)
    B(Redis Node) -->|"football"| A[Server]

    style C fill:#cce5ff,stroke:#004085,stroke-width:2px,color:#000
```
