# Coding Challenge: Building an Agent Swarm

## Introduction

This project is my solution to the CloudWalk Agent Swarm Challenge, focused on building a collaborative multi-agent system. The main objective was to develop an agent swarm capable of processing user requests and generating meaningful responses, utilizing LLM powered agents.

## Challenge Requirements and Implementation

Below, I detail the challenge requirements and how they were addressed in the project's implementation, highlighting what has been completed and what can still be improved.

### Agent Swarm Architecture

The system was designed with an agent swarm architecture, composed of four distinct types of agents, as requested:

*   **Router Agent:** Acts as the primary entry point for user messages. It analyzes the incoming message and decides which specialized agent (or sequence of agents) is best suited to handle it, managing the workflow and data flow between agents.

*   **Knowledge Agent (Source Agent):** Responsible for handling queries that require information retrieval and generation. This agent uses a Retrieval Augmented Generation (RAG) approach to answer questions about the company's products and services, based on content from a specific website. Additionally, it incorporates a web search tool for general-purpose questions.

*   **Customer Support Agent:** Provides customer support, retrieving relevant user data to answer inquiries. Specific tools were implemented for this agent using a fake service that automatically injects the user_id field by the request param which makes the system more robust to agents failure.

*   **Personality Agent (Optional):** A personality layer was applied to refine the final response to the user, making it more human and aligned with the conversation style.

**Implementation Status:** The four agents (Router, Source, Customer Support, and Personality) have been implemented and integrated into a functional workflow. Communication between them is managed by the Router Agent, which directs requests to the appropriate agent.

### API Endpoint

An HTTP endpoint was exposed using FastAPI to accept POST requests with a JSON payload containing the user's message and a `user_id`. This endpoint processes the message through the agent swarm and returns a meaningful JSON response.

**Implementation Status:** The API endpoint is functional and ready to receive requests, orchestrating the interaction with the agents.

### Dockerization

The project was containerized using Docker, with a `Dockerfile` provided to easily and standardly build and run the application.

**Implementation Status:** Containerization was successfully completed, allowing the application to be run using standard Docker commands.

### Testing

Unit tests were developed for agent creation, ensuring they are correctly instantiated. However, the evaluation of agent functionality and performance was not covered by unit or end-to-end tests.

**Implementation Status:** Basic unit tests for agent creation have been implemented. Agent functionality and evaluation tests, as well as end-to-end tests, are areas for future improvement.

### Language and Frameworks

The project was developed in Python, using FastAPI for building the API and LangChain and LangGraph for building the agents and RAG pipeline. For vector store persistence, ChromaDB was used for its practicality.

## Thought Process

In this section, you can describe your thought process during project development, including:

*   **Design and Architecture Choices:** Initially, a supervisor architecture was chosen to ensure clear, single responsibilities for each agent. However, this approach would complicate the later integration of a personality layer, as only the supervisor would interact with the user. To mitigate this, we adopted the swarm architecture provided by LangGraph. We controlled the flow by allowing agents to transfer control only to the router agent (via a handoff tool), and the router, in turn, has handoff tools for the other agents. This ensures each agent is responsible for its own tasks, though there's room for future improvement through customization of the handoff tools and agents themselves, as detailed in [LangGraph Swarm](https://github.com/langchain-ai/langgraph-swarm-py).
*   **RAG Implementation:** The Retrieval-Augmented Generation (RAG) pipeline was implemented using **LangChain** libraries:  

    - `WebBaseLoader` – to ingest documents from URLs  
    - `OpenAIEmbeddings` – to generate embeddings  
    - `ChromaDB` – to persist and query the vector store 
*   **Use of LLM Tools:** The tools were designed to be as simple as possible, with clear descriptions to help agents use them effectively:

    - **RAG** – queries the loaded vector store.  
    - **Web Search** – searches the web, implemented with `Tavily`.  
    - **Handoff Tools** – enable agents to transfer the conversation flow to other agents.  
    - **User Profile and Balance Tools** – implemented as mock services that read from `data/balances.json` and `data/users.json`. Here, `RunnableConfig` was used to inject parameters into the functions, ensuring agents cannot use random IDs or access data from other users. 

## Next Steps and Future Improvements

To enhance this project, the following steps would be considered:

*   **Comprehensive Testing:**
    *   **Unit Tests:** Expand unit tests to cover the internal logic and behavior of each agent, ensuring their individual functionalities operate as expected.
    *   **Integration Tests:** Implement integration tests to verify communication and data flow between different agents, ensuring the swarm functions as a cohesive whole.
    *   **End-to-End (E2E) Tests:** Develop E2E tests for the API endpoint, simulating real user scenarios and validating the responses generated by the complete system. This would include evaluating the quality of agent responses.
    *   **Evaluation Strategy:** Testing agents is complex but essential, especially for production scenarios.  
        The most important next step is to implement automatic evaluators that can assess not only the quality of the answers but also the correctness of the agent flow. To achieve this, I will build a dataset containing both question/answer pairs and the expected agent workflows.  


*   **Handoff and Redirection Mechanisms:**
    *   **Handoff to Humans:** Implement a clear mechanism to redirect complex or unresolved conversations to a human agent.
    *   **Guardrails:** Introduce guardrails to control agent behavior, preventing undesirable or out-of-scope responses and ensuring compliance with security and ethical guidelines.

*   **Monitoring and Observability:**
    *   Implement monitoring and logging tools to track agent performance, identify bottlenecks, and debug issues in real-time.


## How to Run the Project

### Prerequisites

* Docker
* A `.env` file with the required environment variables

### Environment Variables

Create a `.env` file in the root of the project with the following content:
Use the langsmith env variables for tracing with langsmith.

    ```env
    OPENAI_API_KEY=[Open ai API key]
    TAVILY_API_KEY=[Tavily API key]
    LANGSMITH_TRACING=true
    LANGSMITH_ENDPOINT=https://api.smith.langchain.com
    LANGSMITH_API_KEY=[Langsmith API key]
    LANGSMITH_PROJECT=[Langsmith project]
    ```
### Build and Run

1.  **Clone the repository:**
    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd <YOUR_REPOSITORY_NAME>
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t your-agent-project .
    ```

3.  **Run the Docker container:**
    ```bash
    docker run --env-file .env -p 8000:8000 your-agent-project

    ```

    The API will be available at `http://localhost:8000`.

### Running Tests

To run the existing unit tests:

1.  **Access the container (if already running) or build the image and run a shell:**
    ```bash
    docker run --env-file .env -it your-agent-project bash

    ```

2.  **Inside the container, run the tests:**
    ```bash
    poetry run pytest
    ```
