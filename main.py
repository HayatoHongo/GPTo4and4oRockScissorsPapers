import os
import requests
from collections import Counter

API_KEY = os.getenv("OPENAI_API_KEY")
ENDPOINT = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

PROMPT = (
    "You are playing the Rock-Paper-Scissors game. "
    "You should first reason about the Nash equilibrium of this game, "
    "and then choose one action from Rock, Paper, and Scissors based on your reasoning."
)

def query_model(model: str) -> str:
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": PROMPT}],
        "temperature": 1.0,
        "n": 1,
    }
    resp = requests.post(ENDPOINT, headers=HEADERS, json=payload)
    resp.raise_for_status()
    text = resp.json()["choices"][0]["message"]["content"]
    # 回答から「Rock」「Paper」「Scissors」のいずれかを抽出
    for action in ["Rock", "Paper", "Scissors"]:
        if action.lower() in text.lower():
            return action
    return "Unknown"

def run_experiment(model: str, trials: int = 100):
    counter = Counter()
    for _ in range(trials):
        a = query_model(model)
        counter[a] += 1
    print(f"Model: {model}")
    for action in ["Rock", "Paper", "Scissors"]:
        print(f"  {action}: {counter[action]} ({counter[action]/trials:.2%})")

if __name__ == "__main__":
    for m in ["gpt-4o", "o4-mini"]:
        run_experiment(m, trials=100)
