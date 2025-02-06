import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence

# 環境変数の読み込み (.env ファイルから OPENAI_API_KEY を取得)
load_dotenv('./.env.local')



llm = ChatOpenAI(model='gpt-4o-mini', temperature=0, api_key=os.getenv('OPENAI_API_KEY'))
prompt_1 = PromptTemplate(
		input_variables=["user_prompt"],
        # 85トークン
		template="""
        You are a production planner for Manim. Based on the following user prompt, please summarize in bullet points what kind of animations and shapes should be created in Manim.
        User prompt: {user_prompt}
        Output format:
        Shapes and text to be drawn in Manim (including specifications such as color and size)
        Instructions on how the shapes or text should move (animations)
        The general flow of the scene
"""
)


prompt_2 = PromptTemplate(
    input_variables=["instructions"],
    # 147トークン
    template="""
    You are an excellent assistant for generating Manim code.
    Please output executable Python code for Manim based on the following instructions.
    Do not include any unnecessary explanations other than the code.
    Always use from manim import * and class GeneratedScene(Scene): to create the scene.

    Instructions:
    {instructions}

    Output Format:
    python```
    from manim import *

    class GeneratedScene(Scene):
        def construct(self):
            # Required Manim objects and animation calls
            # ...
    ```
    Notes:
    - Always use from manim import * and class GeneratedScene(Scene): format
    - Write all scene-related code inside def construct(self):
    - Do not include any text other than the code
    - You only use the default manim colors
    """
)

chain = RunnableSequence(
    first= prompt_1 | llm,
    last = prompt_2 | llm
)



if __name__ == '__main__':
    output = chain.invoke({"user_prompt": "Draw a circle with a radius of 2 units ..."})
    print("=== FINAL OUTPUT ===")
    print(output.content)
