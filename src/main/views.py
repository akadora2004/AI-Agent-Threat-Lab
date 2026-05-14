from django.shortcuts import render
from openai import OpenAI
import os
from grader import evaluate_report

# Create your views here.

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def index(request):
    score = None
    if request.method == "POST":
        user_input = request.POST.get("user_input")
        score = evaluate_report(user_input)

    return render(request, 'main/index.html', {'score': score})