from dotenv import load_dotenv
load_dotenv()

import os

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain_community.chat_message_histories.upstash_redis import UpstashRedisChatMessageHistory


history = UpstashRedisChatMessageHistory(
    url = os.getenv("UPSTASH_URL"),
    token = os.getenv("UPSTASH_REDIS_REST_TOKEN"),
    session_id = "langchain-chatbot-demo"
    # ttl = 0 # time to live
)

model = ChatOpenAI(
    model = "gpt-4o",
    temperature = 0.7
)


prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly AI assistant."),
    MessagesPlaceholder(variable_name = "chat_history"),
    ("human", "{input}")
])

memory = ConversationBufferMemory(
    memory_key = "chat_history",
    return_messages = True,
    chat_memory = history
)

# chain = prompt | model
chain = LLMChain(
    llm = model, 
    prompt = prompt,
    memory = memory,
    verbose = True
)


msg1 = {
    "input": "I'm a Data Scientist"
}

response1 = chain.invoke(msg1)
print(response1)

msg2 = {
    "input": "What is my occupation?"
}

response2 = chain.invoke(msg2)
print(response2)