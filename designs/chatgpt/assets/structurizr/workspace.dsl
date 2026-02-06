workspace "Name" "Description" {

    !identifiers hierarchical

    model {
        user = person "User"
        chatgptSystem = softwareSystem "ChatGPT System" {
            webServer = container "Web Server" {
                description "Orchestrates prompt lifecycle"
                technology "FastAPI"
            }
            sqlDatabase = container "SQL Database" {
                description "Stores chat conversations and metadata"
                technology "PostgreSQL"
            }
            guardMiddleware = container "Guard Middleware LLM" {
                description "Small LLM fine tuned on guard railing"
                technology "meta-llama/Llama-Guard-3-8B"
            }
            LLM = container "LLMs" {
                technology "OpenAI Models"
                description "Multiple models with different purposes"
            }
            LLMEvaluator = container "LLM Evaluator" {
                description "Traces each prompt lifecycle and raises alerts on violations"
                technology "Langfuse"
            }
        }

        user -> chatgptSystem "Uses for chat conversations with LLMs"
        user -> chatgptSystem.webServer "Uses for chat conversations with LLMs"
        chatgptSystem.webServer -> chatgptSystem.sqlDatabase "Reads from and writes to"
        chatgptSystem.webServer -> chatgptSystem.guardMiddleware "Uses for toxicity / PII sanity checks"
        chatgptSystem.webServer -> chatgptSystem.LLM "Sends and receives prompts from"
        chatgptSystem.webServer -> chatgptSystem.LLMEvaluator "Uses for prompt tracing, monitoring and alerting"
    }

    views {
        systemContext chatgptSystem "ContextDiagram" {
            include *
        }

        container chatgptSystem "ContainerDiagram" {
            include *
        }

        styles {
            element "Element" {
                color #55aa55
                stroke #55aa55
                strokeWidth 7
                shape roundedbox
            }
            element "Person" {
                shape person
            }
            element "Database" {
                shape cylinder
            }
            element "Boundary" {
                strokeWidth 5
            }
            relationship "Relationship" {
                thickness 4
            }
        }
    }

    configuration {
        scope softwaresystem
    }

}