import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

# .envファイルを読み込む
load_dotenv()

ANALYSIS_PROMPT = """あなたはプロの日本株アナリストです。読み手（投資判断の責任者）がすぐ理解できる、簡潔で構造化されたレポートを書いてください。

以下に、銘柄情報・株価データ・関連ニュースを含むレポートを渡します。数日〜数週間のスイングトレードの観点で分析してください。

制約:
- レポートに書かれている情報だけを根拠にすること。書かれていない情報を推測で補ったり、言及したりしないこと
- 各セクションで、判断の根拠にしたレポート内の記述を挙げること
- 株価データの期間とニュースの日付にずれがある場合は、その旨を明記すること

出力は以下のセクション構成のMarkdownで書くこと:
1. 要約（300文字以内）
2. 相場環境: 価格とMA25の推移から、トレンド相場かレンジ相場かの判定
3. テクニカル: MA25と終値の位置関係、トレンドの方向性
4. ニュースセンチメント: ポジティブ／中立／ネガティブの判定と理由
5. 乖離分析: ニュースの内容と株価トレンドの方向が一致しているか矛盾しているか（データの日付ずれで判断できない場合は、判断を保留すると書くこと）
6. エントリー条件: どういう条件が揃えばエントリーを検討できるか（条件ベースで書き、具体的な売買指示はしない）
7. 総合評価: 強気／中立／弱気の見立てと、監視すべきポイント
"""

def analyze_market_data(markdown):

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 環境変数からAPIキーを取得
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": ANALYSIS_PROMPT + "\n--- 以下が分析対象のレポート ---\n" + markdown}],
            timeout=60,
        )
        analysis_result = response.choices[0].message.content

        return analysis_result
    except openai.APIError as e:
        print(f"Error occurred: {e}")
        return None
