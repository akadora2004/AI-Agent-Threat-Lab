import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.openai.iniad.org/api/v1",
)

def evaluate_report(report_text):
    """
    学生のレポートを採点するAIエージェント
    """
    system_prompt = """
    あなたは大学の厳格な採点官です。
    提出された「チームでのアプリ開発において重要だと思うこと」に関するレポートを以下の評価基準をもとに評価してください。

    【評価基準】
    S：以下の要素をすべて含み、極めて優れた考察がなされている。
        - チームメンバーの意見を尊重し、建設的な議論を行っている。
        - 自分の技術力を客観的に把握し、最大限発揮しようとする姿勢がある。
        - 他者の技術力を理解し、適切に連携・フォローを行う。
        - コミュニケーションを欠かさず、チーム全体の進捗に貢献している。
    A：上記の要素の多くを含み、具体的なツール（GitHub, Slack, Docker等）の活用法についても述べられている。
    B：チーム開発の重要性を理解しており、コミュニケーションの必要性について論理的に説明できている。
    C：最低限の内容が含まれているが、具体性や独自の考察が不足している。
    D：内容が不十分であり、チーム開発のメリットや技術的側面への言及がほとんどない。
    E：文章が著しく短く、設問の意図を正しく理解していない。
    F：無回答、または設問と全く無関係な内容である。

    【出力ルール】
    - 評価結果は（S, A, B, C, D, E, F）のいずれか一文字のみを出力してください。
    - 解説やアドバイス、数値などの余計な文字列は一切出力しないでください。
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": report_text}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0
    )

    return response.choices[0].message.content
