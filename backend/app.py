from agent import create_agent
from dotenv import load_dotenv
from fastapi import FastAPI,responses
from langserve import add_routes
from pydantic import BaseModel
from pathlib import Path
from manim_generator import generate_manim_animation

load_dotenv('./.env.local')


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str
    
class Prompt(BaseModel):
    prompt: str
    video_id: str
    



app = FastAPI(
    title='LangChain Server',
    version='1.0',
)

agent = create_agent()

add_routes(
    app,
    agent.with_types(input_type=Input, output_type=Output),
)

@app.get('/api/get_video/{video_id}')
async def get_video(video_id: str):
    path = Path(f'./videos/{video_id}/480p15/GeneratedScene.mp4')
    if not path.exists():
        return responses.JSONResponse(status_code=404, content={'message': 'Video not found'})
    return responses.FileResponse(path,media_type="video/mp4")

@app.post("/api/prompt")
async def prompt(prompt: Prompt):
    prompt = prompt.prompt
    video_id = prompt.video_id
    err = generate_manim_animation(prompt,video_id)
    if err != "Success":
        return responses.JSONResponse(status_code=500, content={'message': err})
    return responses.FileResponse(f'./videos/{video_id}/480p15/GeneratedScene.mp4',media_type="video/mp4")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
