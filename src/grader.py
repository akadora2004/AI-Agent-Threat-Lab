import json
import os
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.iniad.org/api/v1"),
)

GRADE_CHOICES = ["S", "A", "B", "C", "D", "E", "F"]

SYSTEM_PROMPT = """
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

TOOL_PROMPT = """

あなたはデータベース操作ツールを利用できます。
採点後、create_assignment ツールを呼び出して提出内容と評価をデータベースに登録してください。
ツールを使う場合も、評価は（S, A, B, C, D, E, F）のいずれか一文字にしてください。
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "create_assignment",
            "description": "学生の提出内容と評価をデータベースに登録する",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {"type": "integer"},
                    "report_content": {"type": "string"},
                    "grade": {"type": "string", "enum": GRADE_CHOICES},
                },
                "required": ["user_id", "report_content", "grade"],
            },
        },
    },
]


def create_assignment(user_id, report_content, grade):
    from django.contrib.auth.models import User
    from main.models import Assignment

    user = User.objects.get(id=user_id)
    student_name = user.first_name or user.get_full_name() or user.username

    assignment = Assignment.objects.create(
        user=user,
        student_number=user.username,
        student_name=student_name,
        report_content=report_content,
        grade=grade,
    )
    return assignment.grade


def evaluate_report(report_text, user):
    user_prompt = f"ログイン中の user_id: {user.id}\n\n提出内容:\n{report_text}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT + TOOL_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0,
        tools=TOOLS,
        tool_choice="auto",
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return message.content

    for tool_call in message.tool_calls:
        if tool_call.function.name != "create_assignment":
            continue

        args = json.loads(tool_call.function.arguments)
        return create_assignment(**args)

    return message.content
