from langchain.prompts.chat import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langserve import RemoteRunnable

openai_llm = RemoteRunnable("http://localhost:8000/openai/")
anthropic = RemoteRunnable("http://localhost:8000/anthropic/")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "あなたは高学歴で、一般的な言葉を使うのが好きな人です。"
            + "また、あなたは簡潔です。決して3文以上で答えません。",
        ),
        ("human", "好きな小説について教えてください。"),
    ]
).format_messages()

comedian_chain = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "あなたは時に面白いジョークを言うコメディアンであり、時に笑えない事実を述べるだけのコメディアンである。"
                + "ジョークを言うか、事実を述べるか、どちらか一方だけを出力してください。",
            ),
            ("human", "{joke_question}"),
        ]
    )
    | openai_llm
)

joke_classifier_chain = (
    ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "そのジョークが面白いかどうかを判断してください。面白ければ`funny`、"
                + "面白くなけれ ば`not funny`と言ってください。"
                + "そして、参考のためにジョークの最初の5単語を繰り返してください...",
            ),
            ("human", "{joke}"),
        ]
    )
    | anthropic
)


chain = {"joke": comedian_chain} | RunnablePassthrough.assign(
    classification=joke_classifier_chain
)

if __name__ == "__main__":
    print("========openai_model========")
    print(anthropic.invoke(prompt))

    print("======oanthropic_model======")
    print(openai_llm.invoke(prompt))

    print("=======comedian_chain=======")
    print(
        chain.invoke(
            {"joke_question": "こんなエンジニアは嫌だ。どんなエンジニア？"}
        )
    )