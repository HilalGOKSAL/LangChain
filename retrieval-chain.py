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

# docA = Document(
#    page_content = "LangChain Expression Language, or LCEL, is a declarative way to easily compose chains together. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains (we’ve seen folks successfully run LCEL chains with 100s of steps in production)."
# )


def get_documents_from_web(url):
    loader = WebBaseLoader(url) # this clause will scrape the web page and it will then add the content of that page to a langchain document.
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
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


    prompt = ChatPromptTemplate.from_template("""
    Answer the user's question:
    Context : {context}
    Question: {input}
    """)

    # below 2 chain structures are identical, but once we start implementing our retrieval from the
    # data source we will need the create_stuff_documents_chain structure.
    # chain = prompt | model 
    chain = create_stuff_documents_chain(
        llm = model, 
        prompt = prompt,
    )


    retriever = vectorStore.as_retriever(search_kwargs = {"k": 1})

    retrieval_chain = create_retrieval_chain(
        retriever,
        chain
    )

    return retrieval_chain


docs = get_documents_from_web("https://python.langchain.com/v0.1/docs/expression_language/")
vectorStore = create_db(docs)
chain = create_chain(vectorStore)


response = chain.invoke({
    "input" : "What is LCEL?",
})

# print(response)

# print(response["answer"])

print(response["context"])