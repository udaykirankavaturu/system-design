ADR 003: Architectural Style for Chat Quantum (Real-time Engine)

Status: Accepted

1. Problem

The "Chat Quantum" (the core real-time engine managing active socket connections) needs to handle 100M concurrent persistent connections. We need to decide how to structure the application logic to manage this stateful load efficiently.

2.  Objectives

    Connection Density: Maximize the number of concurrent sockets per node.

    Resiliency: If a node dies, user reconnections should not storm the database.

    Latency: Minimal hops between the user and the message delivery.

3.  Alternatives

    Option A: Standard Microservices (Stateless)

        Description: stateless HTTP/WS servers that fetch state (user session, metadata) from Redis/DB for every single event.

    Option B: Space-Based Architecture (Stateful / Actor Model)

        Description: An architecture where the processing unit (Service) holds the state in-memory (RAM) and acts as the "Space" for that user, syncing to DB asynchronously. (e.g., Erlang/Elixir processes or Orleans Grains).

4.  Consequences

    Microservices (Stateless):

        Pros: Easy to deploy and scale; standard pattern (Kubernetes friendly); simple to reason about (request/response).

        Cons: "Chatty" internal traffic—every message triggers a network call to Redis to find "Who is this user?" and "Where is the recipient?"; High latency due to network hops; heavy load on the cache layer.

    Space-Based (Stateful):

        Pros: Data and processing are co-located (Data Locality). Processing a message is near-instant because the user's session is in RAM. Minimal internal network traffic; Database is only for persistence, not for operational reads.

        Cons: Complex to manage (sticky sessions required); rebalancing nodes is hard; higher complexity in deployment and recovery.

5.  Trade-offs (Decision)

Decision: We will use Space-Based Architecture (Stateful/Actor-like). Rationale: For a chat system at 100M concurrent users, the network overhead of fetching session data from Redis for every packet is a massive bottleneck. By treating the Chat Service as a "Space" where the User's Session lives in memory (Stateful), we eliminate the internal network hop. We accept the operational complexity of sticky sessions (via Consistent Hashing on the Load Balancer) to gain the performance benefit of Data Locality. This mimics the architecture of Erlang-based systems like WhatsApp and Discord.
