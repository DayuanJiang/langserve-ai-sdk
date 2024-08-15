from agent import create_agent
from dotenv import load_dotenv
from fastapi import FastAPI
from langserve import add_routes
from pydantic import BaseModel

load_dotenv('../.env.local')


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str


app = FastAPI(
    title='LangChain Server',
    version='1.0',
)
agent = create_agent()

add_routes(
    app,
    agent.with_types(input_type=Input, output_type=Output),
)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host='localhost', port=8000)
