from agent import create_agent
from dotenv import load_dotenv
from fastapi import FastAPI,responses
from langserve import add_routes
from pydantic import BaseModel
from pathlib import Path
from manim_generator import generate_manim_animation
from fastapi.responses import JSONResponse, FileResponse

load_dotenv('./.env.local')

# path名を環境依存
workspace_path =Path("/workspaces/physiquest_animation_generator/backend/media/videos")


class Input(BaseModel):
    input: str


class Output(BaseModel):
    output: str
    
class Prompt(BaseModel):
    user_prompt: str
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
    path =  workspace_path / video_id / "480p15" / "GeneratedScene.mp4"
    if not path.is_file(): 
        return responses.JSONResponse(status_code=404, content={'message': 'Video not found'})
    return responses.FileResponse(path, media_type="video/mp4", filename="GeneratedScene.mp4")

@app.post("/api/prompt",response_class=FileResponse)
async def prompt(prompt: Prompt):
    user_prompt = prompt.user_prompt
    video_id = prompt.video_id
    err = generate_manim_animation(user_prompt,video_id)
    path = workspace_path / video_id / "480p15" / "GeneratedScene.mp4"
    if err != "Success":
        return responses.JSONResponse(status_code=500, content={'message': err})
    return responses.FileResponse(path=path,media_type="video/mp4",filename="GeneratedScene.mp4")




if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='localhost', port=8000)
