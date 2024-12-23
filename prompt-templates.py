from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Instantiate Model
llm = ChatOpenAI(
    model = "gpt-4o",
    temperature = 0.7, 
)

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert Neuropsychologist. Provide scientific findings on the following subject."),
        ("human", "{input}")
    ]
)

# Create LLM Chain
chain = prompt | llm

response = chain.invoke({"input": "sleep cycles"})

print(response)