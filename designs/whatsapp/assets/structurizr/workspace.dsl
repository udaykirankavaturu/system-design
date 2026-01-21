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

        

       
        production = deploymentEnvironment "Production" {
            
            # GLOBAL LAYER
            globalDnsNode = deploymentNode "Global Traffic Manager" "Route53 / Cloudflare" "Global" {
                globalDns = infrastructureNode "GSLB" "Routes traffic to nearest healthy region."
            }

            # REGION A (US)
            regionA = deploymentNode "Region A (US-East)" "Primary Region for Uday" "AWS Region" {
                
                deploymentNode "Load Balancer Layer" {
                    lbInstanceA = containerInstance apiGateway
                }

                deploymentNode "Kubernetes Cluster" "EKS" {
                    chatPodA = containerInstance chatService "x5000 Pods (20k conn/pod)"
                    userPodA = containerInstance userService "x1000 Pods"
                    notifPodA = containerInstance notificationService "x100 Pods"
                }

                deploymentNode "Data Layer" {
                    redisInstanceA = containerInstance redisCluster "Session/Presence Cache"
                    rabbitInstanceA = containerInstance messageBroker "Local Queue"
                    
                    # CASSANDRA NODE (Part of Global Cluster)
                    cassandraInstanceA = containerInstance chatDb "Region A Ring"
                }
            }

            # REGION B (EU)
            regionB = deploymentNode "Region B (EU-West)" "Primary Region for Sam" "AWS Region" {
                
                deploymentNode "Load Balancer Layer" {
                    lbInstanceB = containerInstance apiGateway
                }

                deploymentNode "Kubernetes Cluster" "EKS" {
                    chatPodB = containerInstance chatService "x5000 Pods"
                    userPodB = containerInstance userService "x1000 Pods"
                    notifPodB = containerInstance notificationService "x100 Pods"
                }

                deploymentNode "Data Layer" {
                    redisInstanceB = containerInstance redisCluster "Session/Presence Cache"
                    rabbitInstanceB = containerInstance messageBroker "Local Queue"
                    
                    # CASSANDRA NODE (Part of Global Cluster)
                    cassandraInstanceB = containerInstance chatDb "Region B Ring"
                }
            }

            # RELATIONS FOR DEPLOYMENT
            
            # 1. User Connections
            globalDns -> lbInstanceA "Routes US Traffic"
            globalDns -> lbInstanceB "Routes EU Traffic"
            
            # 2. Cross-Region Data Replication (The "Backbone")
            # cassandraInstanceA -> cassandraInstanceB "Bi-Directional Replication (Async)" "XDC"
            # rabbitInstanceA -> rabbitInstanceB "Federation / Shovel (Forward Events)" "AMQP"
            
            # 3. Local Flows (Region A)
            # chatPodA -> redisInstanceA "Read/Write Session"
            # chatPodA -> cassandraInstanceA "Persist Message"
            # chatPodA -> rabbitInstanceA "Publish 'NewMessage' Event"
            
            # 4. Local Flows (Region B)
            # rabbitInstanceB -> chatPodB "Consume 'NewMessage' Event"
            # chatPodB -> redisInstanceB "Check Local Presence"
        }
    }

    views {
        systemContext whatsapp "Context" {
            include *
            autoLayout tb
        }

        container whatsapp "Containers" {
            include *
        }

        deployment whatsapp "Production" "MultiRegionDeployment" {
            include *
            exclude "relationship.source==chatPodA && relationship.destination==redisInstanceB"
            exclude "relationship.source==chatPodB && relationship.destination==redisInstanceA"
            exclude "relationship.source==chatPodA && relationship.destination==rabbitInstanceB"
            exclude "relationship.source==chatPodB && relationship.destination==rabbitInstanceA"
            exclude "relationship.source==chatPodA && relationship.destination==cassandraInstanceB"
            exclude "relationship.source==chatPodB && relationship.destination==cassandraInstanceA"
            exclude "relationship.source==lbInstanceA && relationship.destination==chatPodB"
            exclude "relationship.source==lbInstanceB && relationship.destination==chatPodA"
            exclude "relationship.source==lbInstanceA && relationship.destination==userPodB"
            exclude "relationship.source==lbInstanceB && relationship.destination==userPodA"
            exclude "relationship.source==rabbitInstanceA && relationship.destination==notifPodB"
            exclude "relationship.source==rabbitInstanceB && relationship.destination==notifPodA"


            
            autoLayout lr
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