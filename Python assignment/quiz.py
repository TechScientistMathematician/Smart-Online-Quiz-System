import os
import random

from rich.console import Console
from rich.table import Table
from rich import box
import utils
import json
import time
from datetime import datetime


def load_questions():
    try:
        with open('data/questions.json', 'r') as f:
            questions = json.load(f)

        # Validate question format
        valid_questions = []
        for q in questions:
            if ('question' in q and 'options' in q and 'correct_answer' in q and
                    len(q['options']) == 4 and q['correct_answer'] in ['A', 'B', 'C', 'D']):
                valid_questions.append(q)

        return random.sample(valid_questions, min(10, len(valid_questions)))

    except FileNotFoundError:
        print("Error: Questions file not found!")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid questions format!")
        return []


def take_quiz(questions):
    user_answers = {}
    start_time = time.time()

    for i, q in enumerate(questions):
        print(f"\nQuestion {i + 1}: {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"{chr(65 + j)}. {option}")

        answer = utils.validate_input(
            "Your answer (A/B/C/D): ",
            ['A', 'B', 'C', 'D']
        )
        user_answers[i] = answer

    time_taken = round(time.time() - start_time)
    return user_answers, time_taken


def calculate_score(questions, user_answers):
    correct = 0
    incorrect = []

    for i, q in enumerate(questions):
        if i in user_answers and user_answers[i] == q['correct_answer']:
            correct += 1
        else:
            incorrect.append({
                'question': q['question'],
                'your_answer': user_answers.get(i, 'Skipped'),
                'correct_answer': q['correct_answer']
            })

    score = (correct / len(questions)) * 100
    print(f"\n===== QUIZ RESULTS =====")
    print(f"Score: {score:.1f}% ({correct}/{len(questions)})")

    # Performance feedback
    if score >= 90:
        feedback = "Excellent!"
    elif score >= 70:
        feedback = "Good!"
    elif score >= 50:
        feedback = "Fair."
    else:
        feedback = "Needs improvement."
    print(f"Performance: {feedback}")

    if incorrect:
        print("\nIncorrect Answers:")
        for item in incorrect:
            print(f"\nQ: {item['question']}")
            print(f"Your answer: {item['your_answer']}")
            print(f"Correct answer: {item['correct_answer']}")

    return score


def save_result(username, score, time_taken):
    try:
        with open('data/leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        leaderboard = []

    leaderboard.append({
        'name': username,
        'score': score,
        'time': time_taken,
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    with open('data/leaderboard.json', 'w') as f:
        json.dump(leaderboard, f)

    print("Result saved to leaderboard!")


def view_leaderboard():
    console = Console()

    try:
        with open('data/leaderboard.json', 'r') as f:
            leaderboard = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        console.print("\n[bold red]Leaderboard is empty![/bold red]")
        console.print("Take a quiz to be the first on the leaderboard! 🏆")
        return

    leaderboard.sort(key=lambda x: (-x['score'], x['time']))
    top_10 = leaderboard[:10]

    table = Table(
        title="🏆 [bold]LEADERBOARD TOP 10[/bold] 🏆",
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        style="cyan"
    )

    table.add_column("Rank", justify="center", style="bold")
    table.add_column("Name", justify="left", style="bold green", min_width=15)
    table.add_column("Score", justify="center", style="bold yellow")
    table.add_column("Time", justify="center", style="bold blue")
    table.add_column("Date", justify="center")


    for i, entry in enumerate(top_10):
        rank_style = "bold"
        if i == 0:
            rank_style = "bold gold1"
        elif i == 1:
            rank_style = "bold silver"
        elif i == 2:
            rank_style = "bold dark_orange3"


        score = entry['score']
        score_style = "bold"
        if score >= 90:
            score_style = "bold green"
        elif score >= 70:
            score_style = "bold yellow"
        elif score >= 50:
            score_style = "bold orange3"
        else:
            score_style = "bold red"

        # 添加行
        table.add_row(
            f"[{rank_style}]{i + 1}[/]",
            f"[bold]{entry['name']}[/]",
            f"[{score_style}]{score:.1f}%[/]",
            f"[bold]{entry['time']}s[/]",
            entry['date']
        )

    console.print("\n")
    console.print(table)

    avg_score = sum(entry['score'] for entry in top_10) / len(top_10)
    best_time = min(entry['time'] for entry in top_10)

    console.print(f"\n[bold]Statistics:[/bold]")
    console.print(f"• Average score of top 10: [bold yellow]{avg_score:.1f}%[/]")
    console.print(f"• Best time: [bold green]{best_time}s[/]")

    user_name = os.getenv("SOQS_USER", "")
    if user_name:
        user_entry = next((e for e in leaderboard if e['name'] == user_name), None)
        if user_entry:
            position = leaderboard.index(user_entry) + 1
            console.print(
                f"\n[bold]Your position:[/bold] [magenta]#{position}[/] with [yellow]{user_entry['score']:.1f}%[/]")