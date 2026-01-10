ADR 002: NoSQL Store for Chat History

Status: Accepted

1. Problem

Having decided on NoSQL (ADR 001), we must select the specific technology. The access pattern is "Write Once, Read Many (Time-Series)". Users typically view the most recent messages. The system requires efficient implementation of the "Inbox" pattern (fetching a slice of messages for a specific conversation ID).

2.  Objectives

    Write Performance: Optimized for append-only logs.

    Read Performance: Extremely fast lookups by ConversationID + Timestamp.

    Operational Maturity: Proven track record at PB scale.

    Multi-DC Replication: Native support for active-active or active-passive replication across regions.

3.  Alternatives

    Option A: MongoDB (Document Store)

    Option B: Cassandra / ScyllaDB (Wide-Column Store)

4.  Consequences

    MongoDB:

        Pros: Flexible JSON documents; intuitive query language; strong developer experience.

        Cons: B-Tree indexes can become heavy on RAM with massive random writes; Global write locking (historically) or complex sharding at extreme scale compared to leaderless replication.

    Cassandra:

        Pros: LSM Tree storage engine is optimized specifically for write-heavy workloads; Leaderless architecture means zero downtime for writes; Linear scalability; Tunable consistency.

        Cons: Rigid modeling (query-first design); No joins or flexible filtering; steeper learning curve.

5.  Trade-offs (Decision)

Decision: We will use Cassandra (or ScyllaDB). Rationale: The data model for chat is essentially a time-series log partitioned by ConversationID. This maps 1:1 with Cassandra's Partition Key (ConversationID) and Clustering Key (MessageID/Timestamp). MongoDB's document model is overkill and less efficient for simple log data. Cassandra's LSM trees provide superior write throughput for our specific "append-only" pattern, and its multi-datacenter replication is industry standard for high availability.
