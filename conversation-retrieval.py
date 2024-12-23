from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.document_loaders import WebBaseLoader
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.chains import create_retrieval_chain

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain.chains.history_aware_retriever import create_history_aware_retriever


import os
os.environ["USER_AGENT"] = "my-app/1.0"  # Replace "my-app/1.0" with an appropriate user-agent string

# docA = Document(
#    page_content = "LangChain Expression Language, or LCEL, is a declarative way to easily compose chains together. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains (we’ve seen folks successfully run LCEL chains with 100s of steps in production)."
# )


def get_documents_from_web(url):
    loader = WebBaseLoader(url) # this clause will scrape the web page and it will then add the content of that page to a langchain document.
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 400,
        chunk_overlap = 20
    )
    splitDocs = splitter.split_documents(docs)
    return splitDocs

def create_db(docs):
    embedding = OpenAIEmbeddings()
    vectorStore = FAISS.from_documents(docs, embedding = embedding)
    return vectorStore


def create_chain(vestorStore):
    model = ChatOpenAI(
        model = "gpt-4o",
        temperature = 0.4
    )


    prompt = ChatPromptTemplate.from_messages([
        ("system" , "Answer the user's questions based on the context: {context}"),
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "{input}")
    ])

    # below 2 chain structures are identical, but once we start implementing our retrieval from the
    # data source we will need the create_stuff_documents_chain structure.
    # chain = prompt | model 
    chain = create_stuff_documents_chain(
        llm = model, 
        prompt = prompt,
    )


    retriever = vectorStore.as_retriever(search_kwargs = {"k": 3})

    retriever_prompt = ChatPromptTemplate.from_messages([
        MessagesPlaceholder(variable_name = "chat_history"),
        ("human", "{input}"),
        ("human", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation.")
    ])

    history_aware_retriever = create_history_aware_retriever(
        llm = model,
        retriever = retriever,
        prompt = retriever_prompt
    )

    retrieval_chain = create_retrieval_chain(
        # retriever,
        history_aware_retriever,
        chain
    )

    return retrieval_chain


def process_chat(chain, question, chat_history):
    response = chain.invoke({
    "input" : question,
    "chat_history" : chat_history
    })

    return response["answer"]

if __name__ == '__main__':
    docs = get_documents_from_web("https://python.langchain.com/v0.1/docs/expression_language/")
    vectorStore = create_db(docs)
    chain = create_chain(vectorStore)

    chat_history = []

    while True: 
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break



        response = process_chat(chain, user_input, chat_history)
        chat_history.append(HumanMessage(content = user_input))
        chat_history.append(AIMessage(content = response))
        print("Assistant: ", response)