from dotenv import load_dotenv
load_dotenv()


from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model = "gpt-4o",
    temperature = 0.7,
    # max_token = 1000,
    # verbose = True 
)

# llm.invoke method allow us to pass prompt and get a response.

# llm.batch - allow us to pass multiple prompts; it allow us to pass list of values
# response = llm.batch(["Hello, how are you?", "Write a poem about AI"])

# llm.stream - allow us to see the output in chunks
response = llm.stream("Write an article about Sleep Cycles")
# print(response)

for chunk in response:
    print(chunk.content, end = "", flush = True)