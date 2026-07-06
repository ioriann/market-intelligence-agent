import openai
import httpx
import src.ai_analysis as ai_analysis


# 偽物のOpenAIクライアント一式。
# 本物と同じ client.chat.completions.create(...) という構造だけ真似ていて、
# create()が呼ばれたら通信せずにAPIError（の子クラス）を投げる
class FakeCompletions:
    def create(self, **kwargs):
        raise openai.APIConnectionError(request=httpx.Request("POST", "https://api.openai.com"))


class FakeChat:
    def __init__(self):
        self.completions = FakeCompletions()


class FakeOpenAI:
    def __init__(self, api_key=None):
        self.chat = FakeChat()


# APIが失敗したとき、クラッシュせずフォールバック文字列が返ることを確認する
def test_analyze_market_data_returns_fallback_on_api_error(monkeypatch):
    monkeypatch.setattr(ai_analysis, "OpenAI", FakeOpenAI)
    result = ai_analysis.analyze_market_data("ダミーレポート")
    assert result == "分析中にエラーが発生しました。"