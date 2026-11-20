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

# Components

```mermaid
%%{init: {'theme': 'forest'}}%%
graph TD
    subgraph Server
        RAM["RAM"]
    end
```

# Characteristics

![Characteristics](./assets/characteristics.png)

# Components revisited for performance

## Write flow

```mermaid
%%{init: {'theme': 'forest'}}%%
graph LR

    subgraph ClientBlock["Client"]
        direction TB
        Client["Client Process"]
    end
    Client["Client Process"] -->|"Write"| ServerIn["Server Process"]

    subgraph Server["Server"]
        direction TB

        ServerIn -->|"(1)"| CommitLog[(Commit log)]
        ServerIn -->|"(2)"| MemoryCache["Memory cache (RAM)"]
        MemoryCache -->|"(3) Flush"| SSTables["SSTables"]

        subgraph MEMORY["MEMORY"]
            MemoryCache
        end

        subgraph DISK["DISK"]
            CommitLog
            SSTables
        end
    end
```

## Read flow

```mermaid
%%{init: {'theme': 'forest'}}%%
%%{init: {'theme': 'forest'}}%%
graph LR
    subgraph ClientBlock["Client"]
        direction TB
        Client["Client Process"]
    end

    subgraph Server["Server"]
        direction TB
        Coordinator["Server Process"]

        subgraph MEMORY["MEMORY"]
            direction LR
            MemoryCache["Memory cache"]
        end

        subgraph DISK["DISK"]
            direction LR
            %% BloomFilter["Bloom filter"] --> SSTables["SSTables"]
        end

        Coordinator -->|"(1) Check memory"| MemoryCache
        MemoryCache -->|"(2) If not in memory"| BloomFilter
        BloomFilter -->|"(3) Find SSTables"| SSTables
        SSTables -.->|"(5) Return result data"| Coordinator
    end

    Client -->|"Read request"| Coordinator
    Coordinator -.->|"(6) Return result"| Client
```

# Components revisited for scalability

## Data partitioning using consistent hashing
- Distribute data evenly
- Minimize data movement when adding or removing nodes.

```mermaid
%%{init: {'theme': 'forest'}}%%
graph TD
    subgraph Ring["Consistent Hash Ring (0 to 359)"]
        direction LR
        N1["Node A (vnodes @ 20, 140, 260)"] -->|"keys 21..80"| N2["Node B (vnodes @ 80, 200, 320)"]
        N2 -->|"keys 81..140"| N1
        N2 -->|"keys 201..260"| N1
        N1 -->|"keys 261..320"| N2
        N2 -->|"keys 321..359 & 0..20"| N1
    end

    subgraph Example["Example: Partitioning by user_id"]
        direction LR
        K1["user_42 -> hash 65"] -->|"walks clockwise to 80"| N2
        K2["user_99 -> hash 125"] -->|"walks clockwise to 140"| N1
        K3["user_15 -> hash 310"] -->|"walks clockwise to 320"| N2
    end

    subgraph Changes["Dynamic Scaling (Add / Remove Node)"]
        direction TB
        Add["Add Node C (@ 110, 230, 350): Only keys in (80..110], (200..230], (320..350] move to Node C"]
        Rem["Remove Node B: Only Node B's vnode key ranges move clockwise to Node A (or C)"]
    end
```
