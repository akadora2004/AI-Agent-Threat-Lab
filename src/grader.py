import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def evaluate_report(report_text):
    """
    学生のレポートを採点するAIエージェント
    """
    system_prompt = """
    あなたは大学の厳格な採点官です。
    提供されたレポートやテキストを読み、論理構成と内容の正確さをS, A, B, C, D, E, Fの7段階で評価してください。
    出力は数値（S, A, B, C, D, E, F）のみを返してください。余計な解説は不要です。
    Sは最高評価, Aは高評価, Bはやや高評価, Cは普通, Dはやや低評価, Eは低評価とし、何も書かれていない場合はFを返してください。
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

if __name__ == "__main__":
    sample = "Pythonは動的な型付けを持つ言語で、可読性が高いのが特徴です。"
    print(f"採点結果: {evaluate_report(sample)}")