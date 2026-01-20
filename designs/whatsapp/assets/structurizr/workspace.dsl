workspace "WhatsApp System Design" "Architecture diagrams for WhatsApp scaling to 1 Billion Users" {

    model {
        # --- Level 1: Context ---
        uday = person "Uday" "User"
        sam = person "Sam" "User"
        
        externalSms = softwareSystem "SMS Service" "Provider for sending SMSes to users." "External"

        whatsapp = softwareSystem "WhatsApp" "System for one to one messaging over the internet." {
            
            # --- Level 2: Containers ---
            
            mobileApp = container "Mobile Client App" "Mobile client to communicate with backend." "iOS + Android / Cross Platform" "Mobile"
            
            apiGateway = container "API Gateway" "Gateway to the multiple backend services." "NGINX / Kong"
            
            # Databases & Brokers
            userDb = container "SQL Database" "Storage for user details." "Postgres" "Database"
            chatDb = container "NoSQL Database for Chat" "Storage with high write throughput." "Apache Cassandra / MongoDB" "Database"
            notifDb = container "NoSQL Database for Notifications" "Storage for notification details and metadata." "MongoDB" "Database"
            redisCluster = container "Redis Cluster" "Contains a cluster of in-memory containers." "Redis" "Database"
            smsCache = container "In-Memory Store" "Storage for SMS limits and metadata." "Redis" "Database"
            messageBroker = container "Message Broker" "Message queue broker for listening to events and processing them." "RabbitMQ" "Queue"

            # Services
            userService = container "User Service" "For user registration, login, profile updates." "Node.js / Java"
            notificationService = container "Notification Service" "Triggers push notifications to users when events happen." "APNS / FCM"
            internalSmsService = container "SMS Service" "Triggers APIs to third party provider for sending SMSes to user." "Node.js"
            
            chatService = container "Chat Service" "Manages chats. Sends messages between users. Saves messages." "Node.js (Socket.io)" {
                
                # --- Level 3: Components (Inside Chat Service) ---
                
                webSocketHandler = component "WebSocket Handler" "For persistent connections between user and server. Validates sessions. Sends messages and saves." "socket.io"
                sessionManager = component "Session Manager" "Checks user's connection server identity. Sends messages to memory to save." "ioredis"
                idGenerator = component "Unique ID Generator" "UUID ID generator for each message." "uuid4"
                cacheManager = component "Cache Manager" "Reads and writes to cache." "ioredis"
                dbClient = component "Database Client" "Writes messages to database." "cassandra-driver"
                eventPublisher = component "Event Publisher" "Adds messages to broker about each message - to notify recipient user." "rabbitmq-client"
            }
        }

        # --- Relationships: C1 Context ---
        uday -> whatsapp "Logs in and maintains active connection" "HTTPS + WebSocket"
        sam -> whatsapp "Logs in and maintains active connection" "HTTPS + WebSocket"
        whatsapp -> externalSms "Makes API calls to trigger SMS" "HTTPS"

        # --- Relationships: C2 Container ---
        mobileApp -> apiGateway "Sends API calls + Websocket connection requests" "HTTPS + WebSocket"
        
        apiGateway -> userService "Makes API calls" "HTTPS"
        apiGateway -> chatService "Makes API calls + Websocket connection requests" "HTTPS + WebSocket"
        
        # User Service Flow
        userService -> userDb "Makes API calls" "HTTPS"
        userService -> internalSmsService "Makes API calls" "HTTPS"
        
        # Chat Service Flow
        chatService -> redisCluster "Makes API calls" "HTTPS"
        chatService -> chatDb "Makes API calls" "HTTPS"
        chatService -> messageBroker "Sends messages for events" "AMQP"
        
        # Notification Flow
        messageBroker -> notificationService "Forwards messages for processing" "AMQP"
        notificationService -> notifDb "Makes API calls" "HTTPS"
        notificationService -> mobileApp "Sends push notifications" "WebSocket/APNS"

        # Internal SMS Flow
        internalSmsService -> smsCache "Makes API calls" "HTTPS"
        internalSmsService -> externalSms "Makes API calls" "HTTPS"
    }

    views {
        systemContext whatsapp "Context" {
            include *
            autoLayout tb
        }

        container whatsapp "Containers" {
            include *
        }

        styles {
            element "Person" {
                shape Person
                background #9accec
                color #000000
            }
            element "Software System" {
                background #7cbfea
                color #000000
            }
            element "Container" {
                background #1168bd
                color #ffffff
            }
            element "Database" {
                shape Cylinder
                background #1168bd
                color #ffffff
            }
            element "Queue" {
                shape Pipe
                background #1168bd
                color #ffffff
            }
            element "Mobile" {
                shape MobileDeviceLandscape
                background #1168bd
                color #ffffff
            }
            element "External" {
                background #888888
                color #ffffff
            }
            element "Component" {
                background #2A76A8
                color #ffffff
            }
        }
    }
}