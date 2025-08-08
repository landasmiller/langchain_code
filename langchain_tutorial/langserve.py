from langchain_google_genai import ChatGoogleGenerativeAI
from fastapi import FastAPI
import uvicorn
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


from langserve import add_routes

system_template = "Translate the following into {language}"

prompt_template = ChatPromptTemplate.from_messages([
    ('system', system_template),
    ('user', '{text}')
])

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", convert_system_message_to_human=True, google_api_key="AIzaSyBd9ANs5-pqdufKa5YnCeCcWNMhMc6dDAM")

parser = StrOutputParser()

chain = prompt_template | model | parser 

app = FastAPI(
    title = "My LLM API",
    description = "My first LLM API",
    version = "0.1.0",
)

add_routes(
    app,
    chain,
    path="/chain"

)

if __name__=="__main__":
    uvicorn.run(app, host="localhost", port=8000)

