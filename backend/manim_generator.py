import os
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.schema.runnable import RunnableSequence
from langchain.output_parsers import RegexParser
import re
from langchain_core.output_parsers import StrOutputParser
import subprocess 
from langchain_core.messages import HumanMessage
import tomllib
# 環境変数の読み込み (.env ファイルから OPENAI_API_KEY を取得)
load_dotenv('./.env.local')
with open("./prompts.toml", 'rb') as f:
    prompts = tomllib.load(f)

def load_llm(model_type:str):
    """
        model_type: str (Gemini Only)
    """
    if os.getenv('OPENAI_API_KEY') is not None:
        llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    else:
        llm = ChatGoogleGenerativeAI(model=model_type, google_api_key=os.getenv('GEMINI_API_KEY'))
    return llm


def general_generate_manim_script(prompt:str):
    think_llm = load_llm("gemini-2.0-flash-thinking-exp")
    pro_llm = load_llm("gemini-2.0-pro-exp")
    prompt_1 = PromptTemplate(
        input_variables=["user_prompt"],
        # 85トークン
		template=prompts["chain"]["prompt1"]
    )
    prompt_2 = PromptTemplate(
        input_variables=["instructions"],
        # 147トークン
        template=prompts["chain"]["prompt2"]
    )
    # parserを作る
    # 正規表現のパターン（`python` で始まり ``` で終わるコードブロックを抽出）
    # 改良版の正規表現
    
    parser = StrOutputParser()
    chain = RunnableSequence(
        first= prompt_1 | think_llm,
        last = prompt_2 | pro_llm | parser
    )
    output =chain.invoke({"user_prompt": prompt})
    # 余分な文字列を削除
    output = output.replace("```python", "")
    output = output.replace("```", "")
    return output


def fix_manim_script_agent(script:str, error:str):
    # エラーメッセージに対して修正を行う。
    llm = load_llm("gemini-2.0-flash-thinking-exp-01-21")
    # いったんllmに修正するためのinstructionを求める
    prompt1 = PromptTemplate(
        input_variables=["script","error"],
        template=prompts["error"]["prompt1"]
    )
    # 修正した
    prompt2 = PromptTemplate(
        input_variables=["instructions"],
        template=prompts["error"]["prompt2"]
    )
    
    parser = StrOutputParser()
    chain = RunnableSequence(
        first= prompt1 | llm,
        last = prompt2 | llm | parser
    )
    print("=== FIX SCRIPT1 ===")
    print("error type", type(error))
    print("script type", type(script))
    
    messages = {"script": script, "error": error}
    
    output = chain.invoke(messages)
    output = output.replace("```python", "").replace("```", "") 
    return output


def script_to_manim_animation(script:str, file_name:str):
    # tmpディレクトリが存在しない場合
    if not os.path.exists("tmp"):
        os.makedirs("tmp")
    with open(f"tmp/{file_name}.py", "w") as f:
        f.write(script)
    # 生成されたManimスクリプトを実行する
    try:
        result = subprocess.run(
                ["manim", "-pql", f"tmp/{file_name}.py", "GeneratedScene"],
                stdout = subprocess.PIPE,
                stderr = subprocess.PIPE,
                text=True,
                check=True)
        return "Success"
    except subprocess.CalledProcessError as e:
        error_message = e.stderr
        error_message = str(error_message)
        return error_message


def script_file_to_manim_animation(file_path:str):
    """
    input:
        file_path: str
    output:
        None or str (error message)
    
    スクリプトファイルが存在する場合にそのファイルをmanimにより実行して、生成する。
    """
    # 生成されたManimスクリプトを実行する
    try:
        reslut=subprocess.run(
                        ["manim", "-pql", f"{file_path}", "GeneratedScene"], 
                        stdout=subprocess.PIPE,  # 標準出力をキャプチャ
                        stderr=subprocess.PIPE,  # 標準エラーをキャプチャ
                        text=True,  # 出力を文字列として取得
                        check=True
                )
        return "Success"
    except subprocess.CalledProcessError as e:
        error_message = e.stderr  # 標準エラーの全文を取得
        return error_message




def generate_manim_animation(prompt:str, file_name:str, instruction_type:int):
    output = general_generate_manim_script(prompt)
    err=script_to_manim_animation(output, file_name)
    return err


def manim_script_error_handler(script:str, error:str ,file_name:str):
    output = fix_manim_script_agent(script, error)
    error = script_to_manim_animation(output, file_name)
    return error

def generate_manim_animation_with_error_handling(prompt:str,file_name:str):
    output = general_generate_manim_script(prompt)
    err = script_to_manim_animation(output, file_name)
    # スクリプトの修正回数
    count = 0 
    while err != "Success":
        output = fix_manim_script_agent(output, err)
        err = script_to_manim_animation(output, file_name)
        print(count)
        count += 1
        if count > 5:
            return "Error: Failed to fix the script"
    return err



if __name__ == '__main__':
    # テストコード テストクリア
    with open("tmp/test_2.py") as f:
        content = f.read()
    
    error = script_file_to_manim_animation("tmp/test_2.py")
    fine_id = "test_2"
    count = 0
    while error != "Success":
        error = manim_script_error_handler(content, error, fine_id)
        print(error)
        count += 1
        if count > 5:
            print("Error: Failed to fix the script")
            break

