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

# Components revisited for high availability

## CAP Theorem

```mermaid
%%{init: {'theme': 'forest'}}%%
graph TD
    CAP["<b>CAP Theorem</b><br/><i>In a distributed system, pick at most 2 during a network failure</i>"]

    C["<b>Consistency (C)</b><br/>All nodes see the exact same data at the same time"]
    A["<b>Availability (A)</b><br/>Every request receives a non-error response (without guarantee of latest data)"]
    P["<b>Partition Tolerance (P)</b><br/>System continues operating despite network splits/dropped messages between nodes"]

    CAP --- C
    CAP --- A
    CAP --- P

    C & P --> CP["<b>CP Systems</b><br/><i>Sacrifices Availability during partition</i><br/>• Rejects writes/reads if quorum unreachable<br/>• Examples: HBase, MongoDB, Redis Cluster"]
    A & P --> AP["<b>AP Systems</b><br/><i>Sacrifices Strict Consistency during partition</i><br/>• Returns most recent available version (Eventual Consistency)<br/>• Examples: Cassandra, DynamoDB, CouchDB"]
    C & A --> CA["<b>CA Systems</b><br/><i>No Partition Tolerance (Not realistic for distributed networks)</i><br/>• Single-node or non-partitioned setups<br/>• Examples: Traditional RDBMS (PostgreSQL, MySQL)"]
```

## Data replication and data consistency

```mermaid
%%{init: {'theme': 'forest'}}%%
graph TD
    subgraph Failover["Scenario 2: Node B Down (Sloppy Quorum & Hinted Handoff)"]
        direction LR
        C2["Client"] -->|"Write (user_42)"| Coord2["Coordinator"]
        Coord2 -->|"Primary write"| N2_A["Node A (Primary)"]
        Coord2 -.->|"Timeout / Unreachable"| N2_B["Node B (DOWN)"]
        Coord2 -->|"Replica write"| N2_C["Node C (Replica 2)"]
        Coord2 -->|"Temporary write + Hint for B"| N2_D["Node D (Standby / Hinted Handoff)"]
        N2_A & N2_C & N2_D -.->|"ACK (Quorum W=2 met)"| Coord2
        Coord2 -.->|"200 OK (Still Available!)"| C2
        N2_D -.->|"Replays write when Node B recovers"| N2_B
    end

    subgraph Healthy["Scenario 1: All Nodes Healthy (Normal Replication)"]
        direction LR
        C1["Client"] -->|"Write (user_42)"| Coord1["Coordinator"]
        Coord1 -->|"Primary write"| N1_A["Node A (Primary)"]
        Coord1 -->|"Replica write"| N1_B["Node B (Replica 1)"]
        Coord1 -->|"Replica write"| N1_C["Node C (Replica 2)"]
        N1_A & N1_B & N1_C -.->|"ACK (Quorum W=2 met)"| Coord1
        Coord1 -.->|"200 OK"| C1
    end
```

## Data inconsistency handling

```mermaid
%%{init: {'theme': 'forest'}}%%
graph LR
    Start["<b>1. Initial Write</b><br/>Client writes data = 'v1'<br/>Handled by Node Sx<br/><b>D1: [Sx, 1]</b>"] --> Split

    Split{"<b>2. Concurrent Writes (Network Partition / Race)</b><br/>Two clients update D1 simultaneously"}

    Split -->|"Client 1 writes 'v2' on Sy"| D2["<b>D2: [Sx, 1], [Sy, 1]</b><br/><i>Ancestor: D1</i>"]
    Split -->|"Client 2 writes 'v3' on Sz"| D3["<b>D3: [Sx, 1], [Sz, 1]</b><br/><i>Ancestor: D1</i>"]

    D2 & D3 --> Read["<b>3. Later Read Request</b><br/>Client reads both D2 and D3 from replicas"]

    Read --> Compare{"<b>4. Vector Clock Comparison</b><br/>Is every counter in one >= the other?"}

    Compare -->|"No: Sy has 1 vs 0, Sz has 0 vs 1<br/>(Neither is an ancestor of the other)"| Conflict["<b>5. Conflict Detected!</b><br/>Siblings D2 & D3 returned to Client"]

    Conflict --> Resolve["<b>6. Client-Side Resolution</b><br/>Client merges 'v2' + 'v3' -> 'v4'<br/>Writes back via Sx:<br/><b>D4: [Sx, 2], [Sy, 1], [Sz, 1]</b>"]
```

## Handling permanent failure

```mermaid
%%{init: {'theme': 'forest'}}%%
graph TD
    subgraph Detection["Phase 1: Failure Detection (Gossip Protocol)"]
        direction LR
        G1["<b>1. Periodic Heartbeat Exchange</b><br/>Each node maintains a membership list<br/><i>[Node ID, Heartbeat Counter, Timestamp]</i>"]
        G1 --> G2["<b>2. Random Peer Gossip</b><br/>Every second, Node A sends its table<br/>to random peers (Node C, Node D)"]
        G2 --> G3["<b>3. Stale Heartbeat Check</b><br/>Node B's heartbeat counter stops<br/>incrementing past <i>t_fail</i> threshold"]
        G3 --> G4["<b>4. Confirmed Permanent Failure</b><br/>Cluster marks Node B <b>DOWN</b>;<br/>ring shifts Node B's range to Node C"]
    end

    subgraph Sync["Phase 2: Replica Sync (Anti-Entropy via Merkle Trees)"]
        direction LR
        M1["<b>1. Build Hash Trees per Key Range</b><br/>Node A and Node C build Merkle trees<br/>over their shared partition keys"]
        M1 --> M2["<b>2. Compare Root Hashes</b><br/>Root_A != Root_C -> mismatch detected"]
        M2 --> M3["<b>3. Traverse Differing Branches</b><br/>Compare child hashes down the tree,<br/>skipping identical subtrees"]
        M3 --> M4["<b>4. Stream Missing Keys Only</b><br/>Identify divergent leaf bucket (e.g., <i>user_42</i>)<br/>and sync only those records"]
    end

    Detection ==>|"Triggers rebalancing & background repair"| Sync
```
