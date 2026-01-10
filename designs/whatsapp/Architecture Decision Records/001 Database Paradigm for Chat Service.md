ADR 001: Database Paradigm for Chat Service

Status: Accepted

1. Problem

The Chat Service must ingest and store incoming messages at a scale of 1 Million writes per second (1M QPS). We need a database paradigm that can handle massive write throughput while maintaining low latency for message retrieval. Traditional relational models may struggle with this volume of concurrent writes. 2. Objectives

    Write Throughput: Must support >1M concurrent writes/sec.

    Scalability: Must support horizontal scaling (sharding) without complex manual operations.

    Availability: System must remain writable even if individual nodes fail (AP over CP preferred).

    Schema Flexibility: Ability to evolve message metadata without locking tables.

3.  Alternatives

    Option A: SQL (Relational Database - e.g., PostgreSQL/MySQL)

    Option B: NoSQL (Non-Relational Database - e.g., Cassandra/DynamoDB)

4.  Consequences

    SQL:

        Pros: ACID compliance ensures strong consistency; rich query capabilities; mature tooling.

        Cons: Scaling writes horizontally (sharding) is complex and operationally expensive at this scale; rigid schema requires downtime or heavy locks for migrations.

    NoSQL:

        Pros: Native horizontal partitioning (sharding) allows linear scaling of write throughput; flexible schema; optimized for high velocity data; often tunable consistency.

        Cons: Eventual consistency can be tricky; limited query patterns (no complex joins).

5.  Trade-offs (Decision)

Decision: We will use NoSQL. Rationale: The primary bottleneck is Write Throughput. SQL databases typically hit a ceiling on write IOPS that requires complex sharding solutions (like Vitess) to bypass. NoSQL databases are designed from the ground up to distribute writes across a cluster. We are willing to trade ACID transactions and complex joins (which we don't need for simple message logs) in exchange for massive write scalability and high availability.
