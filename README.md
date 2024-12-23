# LangChain Utilities

This repository contains Python scripts showcasing various functionalities and utilities built using the [LangChain framework](https://www.langchain.com/). The tools and examples provided demonstrate how to leverage LangChain for conversational AI, retrieval-augmented generation (RAG), memory management, output parsing, and prompt templates.

## Table of Contents

- [Overview](#overview)
- [Requirements](#requirements)
- [Setup](#setup)
- [Scripts](#scripts)
  - [agent.py](#agentpy)
  - [conversation-retrieval.py](#conversation-retrievalpy)
  - [llm.py](#llmpy)
  - [memory.py](#memorypy)
  - [output-parser.py](#output-parserpy)
  - [prompt-template.py](#prompt-templatepy)
- [How to Run](#how-to-run)

## Overview

The repository contains the following Python scripts:

1. **agent.py**: Implements an OpenAI-based conversational agent using tools like web retrieval and custom embeddings.
2. **conversation-retrieval.py**: Demonstrates retrieval-augmented generation using FAISS vector stores and history-aware retrieval.
3. **llm.py**: Contains examples of using the ChatOpenAI API for basic language model interaction.
4. **memory.py**: Implements a conversation buffer memory with Upstash Redis for chat message persistence.
5. **output-parser.py**: Demonstrates different types of output parsers (string, list, JSON) using LangChain.
6. **prompt-template.py**: Illustrates prompt template usage to customize and structure input prompts.

## Requirements

- Python 3.8+
- Required Python libraries (see `requirements.txt`):
  - `langchain`
  - `dotenv`
  - `pydantic`
  - `beautifulsoup4`
  - `faiss`
  - `openai`

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add the following keys:
   ```env
   OPENAI_API_KEY=<your_openai_api_key>
   UPSTASH_URL=<your_upstash_redis_url>
   UPSTASH_REDIS_REST_TOKEN=<your_upstash_redis_token>
   USER_AGENT=my-app/1.0
   ```

## Scripts

### agent.py

This script creates a conversational agent called **Max** that can answer user queries using:
- Web data retrieval from LangChain Expression Language documentation.
- FAISS vector store for embeddings and similarity search.

#### Key Features:
- Leverages `TavilySearchResults` for external search queries.
- Processes conversation context with a custom `AgentExecutor`.

Run the script and interact with the agent:
```bash
python agent.py
```

### conversation-retrieval.py

Demonstrates retrieval-augmented generation with:
- Web scraping using `WebBaseLoader`.
- Chunking and splitting documents for embeddings.
- History-aware retrieval to refine context-aware responses.

Run the script to interact with the retrieval system:
```bash
python conversation-retrieval.py
```

### llm.py

Contains examples for:
- Single-prompt interaction with `llm.invoke`.
- Batch processing for multiple prompts.
- Streaming responses for large outputs.

Run the script to see LLM streaming responses:
```bash
python llm.py
```

### memory.py

Implements conversation memory using `ConversationBufferMemory` with Upstash Redis for persistent storage. Demonstrates maintaining context across multiple interactions.

Run the script to test memory management:
```bash
python memory.py
```

### output-parser.py

Showcases various output parsers:
- `StrOutputParser` for plain string outputs.
- `CommaSeparatedListOutputParser` for lists.
- `JsonOutputParser` for structured JSON responses with Pydantic validation.

Run the script to see output parsing examples:
```bash
python output-parser.py
```

### prompt-template.py

Illustrates the use of prompt templates to:
- Define dynamic input variables.
- Customize system and user instructions for better responses.

This script provides a foundational structure for crafting effective prompts.

## How to Run

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

2. Run any of the scripts with:
   ```bash
   python <script-name>.py
   ```

3. Follow the on-screen instructions to interact with the AI or retrieve results.

## Notes

- Ensure your `.env` file contains valid API keys and credentials for OpenAI and Upstash.
- Some scripts rely on external web scraping and may require stable internet access.
- For further customization, refer to the LangChain documentation.
