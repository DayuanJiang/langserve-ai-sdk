import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv
import tomllib
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnableSequence
from langchain_core.output_parsers import StrOutputParser

load_dotenv('./.env.local')

class ManimAnimationService:
    def __init__(self):
        with open("./prompts.toml", 'rb') as f:
            self.prompts = tomllib.load(f)
        self.think_llm = self._load_llm("gemini-2.0-flash-thinking-exp")
        self.pro_llm   = self._load_llm("gemini-2.0-pro-exp")
    
    def _load_llm(self, model_type: str):
        if os.getenv('OPENAI_API_KEY'):
            return ChatOpenAI(model='gpt-4o-mini', temperature=0)
        return ChatGoogleGenerativeAI(model=model_type, google_api_key=os.getenv('GEMINI_API_KEY'))
    
    def generate_script(self, user_prompt: str) -> str:
        prompt1 = PromptTemplate(
            input_variables=["user_prompt"],
            template=self.prompts["chain"]["prompt1"]
        )
        prompt2 = PromptTemplate(
            input_variables=["instructions"],
            template=self.prompts["chain"]["prompt2"]
        )
        parser = StrOutputParser()
        chain = RunnableSequence(
            first= prompt1 | self.think_llm,
            last = prompt2 | self.pro_llm | parser
        )
        output = chain.invoke({"user_prompt": user_prompt})
        return output.replace("```python", "").replace("```", "")
    
    def run_script(self, file_name: str, script: str) -> str:
        if not os.path.exists("tmp"):
            os.makedirs("tmp")
        tmp_path = Path(f"tmp/{file_name}.py")
        with open(tmp_path, "w") as f:
            f.write(script)
        try:
            subprocess.run(
                ["manim", "-pql", str(tmp_path), "GeneratedScene"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, check=True
            )
            return "Success"
        except subprocess.CalledProcessError as e:
            return e.stderr

    def fix_script(self, script: str, error: str, file_name: str) -> str:
        prompt1 = PromptTemplate(
            input_variables=["script", "error"],
            template=self.prompts["error"]["prompt1"]
        )
        prompt2 = PromptTemplate(
            input_variables=["instructions"],
            template=self.prompts["error"]["prompt2"]
        )
        parser = StrOutputParser()
        chain = RunnableSequence(
            first= prompt1 | self.think_llm,
            last = prompt2 | self.think_llm | parser
        )
        messages = {"script": script, "error": error}
        output = chain.invoke(messages)
        return output.replace("```python", "").replace("```", "")

    def generate_animation_with_error_handling(self, user_prompt: str, file_name: str) -> str:
        script = self.generate_script(user_prompt)
        err = self.run_script(file_name, script)
        count = 0
        while err != "Success" and count < 5:
            script = self.fix_script(script, err, file_name)
            err = self.run_script(file_name, script)
            count += 1
        return err

    def run_script_file(self, file_path: Path, file_name: str) -> str:
        try:
            subprocess.run(
                ["manim", "-pql", str(file_path), "GeneratedScene"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True, check=True
            )
            return "Success"
        except subprocess.CalledProcessError as e:
            return e.stderr

