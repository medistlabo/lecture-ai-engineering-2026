from types import SimpleNamespace

from app import ask as ask_module


class FakeChat:
    def __init__(self):
        self.questions = []

    def send_message(self, question):
        self.questions.append(question)
        return SimpleNamespace(
            text=f"回答: {question}",
            usage_metadata=SimpleNamespace(prompt_token_count=1, candidates_token_count=2),
        )


class FakeClient:
    def __init__(self, chat):
        self.chats = SimpleNamespace(create=lambda model: chat)


def test_ask_sends_question_to_existing_chat():
    chat = FakeChat()

    answer = ask_module.ask("最初の質問", chat)

    assert answer == "回答: 最初の質問"
    assert chat.questions == ["最初の質問"]


def test_ask_prints_response_time_and_token_counts(monkeypatch, capsys):
    chat = FakeChat()
    timestamps = iter([10.0, 10.25])
    monkeypatch.setattr(ask_module, "perf_counter", lambda: next(timestamps))

    ask_module.ask("質問", chat)

    output = capsys.readouterr().out
    assert "[metrics] response time: 0.25s" in output
    assert "input tokens: 1, output tokens: 2" in output


def test_main_keeps_one_chat_for_follow_up_questions(monkeypatch, capsys):
    chat = FakeChat()
    client = FakeClient(chat)
    monkeypatch.setattr(ask_module.genai, "Client", lambda api_key: client)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr("sys.argv", ["app.ask", "最初の質問"])
    questions = iter(["続きの質問", ""])
    monkeypatch.setattr("builtins.input", lambda _prompt: next(questions))

    ask_module.main()

    assert chat.questions == ["最初の質問", "続きの質問"]
    output = capsys.readouterr().out
    assert "回答: 最初の質問" in output
    assert "回答: 続きの質問" in output
