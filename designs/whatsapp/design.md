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
- user should be notified when a new message arrives

# Non functional requirements

- scalability
  - daily active users (DAU) - 1 billion
  - queries per second (QPS) - 1 million
  - peak qps - 100 million
  - storage @ 1kb per message - retention of 7 days
    - 2.1 PB (see [storage calcuation](./assets/storage%20calculation.png))
-
