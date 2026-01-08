# System design for 'whatsapp'

whatsapp is a communicator app - it includes 1:1 messaging, group chats, 1:1 calling, group calls, sharing files, backups, payment and more.

# Restricting scope for system design

## In scope

- registration and authentication (high level)
- focus on 1:1 messaging
- notifications (high level)

## Out of scope

- everything else

# Functional requirements

- system should allow registration of new users
- system should allow authentication of existing users
- user should be able to send text message via internet to other users on the platform
- user should be able to receive text message from other users
- user should be notified when a new message arrives in near real time

# Non functional requirements

- scalability
  - daily active users (DAU) - 1 billion
  - queries per second (QPS) - 1 million
  - peak qps - 100 million
  - storage @ 1kb per message - retention of 7 days
    - ~2.1 PB (see [storage calcuation](./assets/storage%20calculation.png))
- performance
  - <500 ms
- availability
  - 99.99% for chat, 99.9% for notifications
- durability
  - messages are never lost
- consistency
  - messages are delivered in sequence

# Actors Actions

![Diagram](./assets/actors%20actions.png)

# Event Storming

![Diagram](./assets/event%20storming.png)

# Workflow

![Diagram](./assets/workflow.png)

# Components

![Diagram](./assets/components.png)

# Characteristics

![Diagram](./assets/characteristics.png)

# Quanta

![Diagram](./assets/quanta.png)

# Architecture Styles

![Diagram](./assets/architecture%20styles.png)

# C1

![Diagram](./assets/c1.png)

# C2

![Diagram](./assets/c2.png)

#
