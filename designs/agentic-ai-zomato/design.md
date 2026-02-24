# System design for an agentic AI system

Build an agentic AI system for ordering food on zomato.

# Functional requirements

- user should be able to chat with zomato
- user should be able to browse menus, restaurants
- user should be able to add items to cart
- user should be able to make payment to complete the order
- user should be able to track the order status
- system should process the order and deliver it
- user should be able to go back to previous chats and continue the conversation
- only authenticated users can place orders

## Non functional requirements

- scalability
  - daily-active users (DAU): 100M.
  - number of restaurants: 500M.
  - search requests per day: 10x of DAU.
- elasticity
  - peak during breakfast, lunch, dinner times
  - peak QPS - 1 million
- availability
  - 99.99% for chat
- data integrity
  - messages are never lost
- fault tolerant
  - when chat breaks, handle appropriately
  - user should be able to start a new conversation and continue (system should not break)
- deployability
- system should be easily deployable
- abstraction
- LLMs should not provide information outside of zomato context
- LLMs should not provide information about other users
- security
- LLMs should be safe and non-toxic, PIIs must be handled
