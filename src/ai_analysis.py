import os
from dotenv import load_dotenv
from openai import OpenAI

# .envファイルを読み込む
load_dotenv()

def analyze_market_data(markdown):

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # 環境変数からAPIキーを取得
    response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[{"role": "user", "content": "株式を分析してください" + "\n\n以下はレポートです:\n" + markdown}],  # プロンプトは要改善
    )
    analysis_result = response.choices[0].message.content

    return analysis_result
