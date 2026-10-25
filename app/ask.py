"""第1回: 素のLLMに質問し、会話を続けるスクリプト。

使い方:
    uv run python -m app.ask "LoRAとは何ですか？"
    uv run python -m app.ask            # 質問を省略すると、講座に固有の質問をする

空行を入力するまで、同じ会話の履歴を保ったまま続けて質問できる。
ツールを持たない「素の」呼び出し。
講座に固有のことを聞くと、「分からない」と答えるか、一般論でもっともらしく答える
（講座の実際とは違う）ことを確かめよう。
（第3回で、用語集を検索できるエージェントにして改善する）
"""

import argparse
from time import perf_counter

from google import genai
from google.genai import errors

from app.config import MODEL, api_error_message, get_api_key

# 講座に固有の質問。正しい答えは data/glossary.json の homework-levels にある
DEFAULT_QUESTION = "AIE2026の講座の宿題にある「3レベル」とは何ですか？"


def ask(question: str, chat=None) -> str:
    if chat is None:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
    started_at = perf_counter()
    response = chat.send_message(question)
    elapsed = perf_counter() - started_at

    usage = response.usage_metadata
    input_tokens = usage.prompt_token_count if usage is not None else "unavailable"
    output_tokens = usage.candidates_token_count if usage is not None else "unavailable"
    print(
        f"[metrics] response time: {elapsed:.2f}s, "
        f"input tokens: {input_tokens}, output tokens: {output_tokens}"
    )

    return response.text


def main() -> None:
    parser = argparse.ArgumentParser(description="素のLLMに質問する")
    parser.add_argument("question", nargs="?", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    print(f"[model] {MODEL}")
    question = args.question
    try:
        client = genai.Client(api_key=get_api_key())
        chat = client.chats.create(model=MODEL)
        while True:
            print(f"[質問] {question}\n")
            print(ask(question, chat))
            try:
                question = input("\n続けて質問してください（終了するには空行）: ")
            except EOFError:
                break
            if not question.strip():
                break
    except errors.APIError as e:
        print(api_error_message(e.code, e.message))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
