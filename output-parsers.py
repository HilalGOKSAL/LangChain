from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, CommaSeparatedListOutputParser, JsonOutputParser
from pydantic import BaseModel, Field

model = ChatOpenAI(model = "gpt-4o", temperature = 0.7)

def call_string_output_parser():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Tell me a psychological effect about following subject"),
            ("human", "{input}")
        ]
    )
    parser = StrOutputParser()

    chain = prompt | model | parser

    return chain.invoke({
        "input" : "romantic relationship"
    })

# print(call_string_output_parser())

def call_list_output_parser():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Generate a list of 10 synonyms for the following word. Return the results as a comma seperated list."),
        ("human", "{input}")
    ])

    parser = CommaSeparatedListOutputParser()
    
    chain = prompt | model | parser

    return chain.invoke({
        "input": "happy"
    })
    
# print(call_list_output_parser())


# In order for model to understand how to extract the information and assign it to dictionary properties,
# we need to provide it with formatting instructions. We won't have to manually type out instructions. But they will be generated
# for us by using a pydantic class. 

def call_json_output_parser():
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Extract information from the following phrase. \nFormatting Instructions: {format_instructions}"),
        ("human", "{phrase}")
    ])

    class Person(BaseModel):
        name: str = Field(description = "the name of the person")
        age: int = Field(description = "the age of the person")

    # This parser expect us to pass in the definition or the schema of that JSON structure.
    # The way we can easily define that JSON structure is by using the pydantic object.
    parser = JsonOutputParser(pydantic_object = Person)

    chain = prompt | model | parser

    return chain.invoke({
        "phrase" : "Max is 30 years old",
        "format_instructions": parser.get_format_instructions()
    })

print(call_json_output_parser())