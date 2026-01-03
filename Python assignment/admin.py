import json
import os
import random
import smtplib
from datetime import datetime, timedelta
from email.mime.text import MIMEText

import config

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', '0xxxcxy@gmail.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'famg cawu vajh bgjn')

otp_store = {}


def send_otp_email(email):
    otp = str(random.randint(100000, 999999))
    expiration = datetime.now() + timedelta(minutes=10)

    otp_store[email] = {
        'otp': otp,
        'expires': expiration.timestamp()
    }

    try:
        msg = MIMEText(f"Your OTP for SOQS password reset is: {otp}\n\nThis code expires in 10 minutes.")
        msg['Subject'] = 'SOQS Password Reset OTP'
        msg['From'] = SMTP_USER
        msg['To'] = email

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return True, "OTP sent successfully"
    except Exception as e:
        return False, f"Failed to send OTP: {str(e)}"


def verify_otp(email, user_otp):
    if email not in otp_store:
        return False, "OTP not requested or expired"

    otp_data = otp_store[email]

    if datetime.now().timestamp() > otp_data['expires']:
        del otp_store[email]
        return False, "OTP expired"

    if user_otp == otp_data['otp']:
        del otp_store[email]
        return True, "OTP verified"

    return False, "Invalid OTP"


def reset_password_workflow():
    config_data = config.get_config()

    if not config_data.get('admin_email'):
        print("No admin email configured. Please contact system administrator.")
        return False

    admin_email = config_data['admin_email']

    print("\n=== Password Reset ===")
    print(f"Security Question 1: {config_data['security_questions']['question1']}")
    answer1 = input("Your answer: ").strip()
    print(f"\nSecurity Question 2: {config_data['security_questions']['question2']}")
    answer2 = input("Your answer: ").strip()

    answers_hash = config.hash_value(f"{answer1}_{answer2}")
    if answers_hash != config_data.get('answers_hash', ''):
        print("Security answers do not match!")
        return False

    print("\nSending OTP to your admin email...")
    success, message = send_otp_email(admin_email)
    print(message)
    if not success:
        return False

    user_otp = input("Enter OTP from your email: ").strip()
    success, message = verify_otp(admin_email, user_otp)
    print(message)
    if not success:
        return False

    while True:
        new_password = input("Enter new password: ").strip()
        confirm_password = input("Confirm new password: ").strip()

        if new_password != confirm_password:
            print("Passwords do not match!")
            continue

        valid, msg = config.validate_password(new_password)
        if not valid:
            print(msg)
            continue

        config_data['password_hash'] = config.hash_value(new_password)
        config.save_config(config_data)
        print("Password reset successfully!")
        return True


def admin_login():
    config_data = config.get_config()

    if not config_data.get('admin_email') or not config_data.get('password_hash'):
        print("\n=== First-Time Admin Setup ===")
        admin_email = input("Enter admin email: ").strip()

        print(f"\nSecurity Question 1: {config_data['security_questions']['question1']}")
        answer1 = input("Your answer: ").strip()
        print(f"\nSecurity Question 2: {config_data['security_questions']['question2']}")
        answer2 = input("Your answer: ").strip()

        while True:
            password = input("Set admin password: ").strip()
            confirm = input("Confirm password: ").strip()

            if password != confirm:
                print("Passwords do not match!")
                continue

            valid, msg = config.validate_password(password)
            if not valid:
                print(msg)
                continue

            config_data['admin_email'] = admin_email
            config_data['password_hash'] = config.hash_value(password)
            config_data['answers_hash'] = config.hash_value(f"{answer1}_{answer2}")
            config.save_config(config_data)
            print("Admin setup complete!")
            return True

    attempts = 0
    while attempts < 3:
        password = input("Enter admin password: ").strip()

        if config.hash_value(password) == config_data['password_hash']:
            return True

        attempts += 1
        print(f"Invalid password! Attempts remaining: {3 - attempts}")

    print("\nForgot your password?")
    if input("Reset password? (y/n): ").lower() == 'y':
        return reset_password_workflow()

    return False


def admin_menu():
    if not admin_login():
        print("Admin login failed.")
        return

    while True:
        print("\n===== ADMIN PANEL =====")
        print("1. Add New Question")
        print("2. Search Questions")
        print("3. Exit Admin")

        choice = input("Enter choice: ")

        if choice == '1':
            add_question()
        elif choice == '2':
            search_questions()
        elif choice == '3':
            break
        else:
            print("Invalid choice!")


def add_question():
    print("\n-- Add New Question --")
    question = input("Enter question: ").strip()

    options = []
    for i in range(4):
        options.append(input(f"Enter option {chr(65 + i)}: ").strip())

    while True:
        correct = input("Correct answer (A/B/C/D): ").upper()
        if correct in ['A', 'B', 'C', 'D']:
            break
        print("Invalid choice!")

    try:
        with open('data/questions.json', 'r') as f:
            questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        questions = []

    if any(q['question'].lower() == question.lower() for q in questions):
        print("Error: Identical question already exists!")
        return

    questions.append({
        'question': question,
        'options': options,
        'correct_answer': correct
    })

    with open('data/questions.json', 'w') as f:
        json.dump(questions, f)

    print("Question added successfully!")


def search_questions():
    try:
        with open('data/questions.json', 'r') as f:
            questions = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("No questions available!")
        return

    keyword = input("Enter search keyword: ").lower()
    results = [q for q in questions if keyword in q['question'].lower()]

    if not results:
        print("No matching questions found!")
        return

    print(f"\nFound {len(results)} matching questions:")
    for i, q in enumerate(results):
        print(f"\n{i + 1}. {q['question']}")
        for j, option in enumerate(q['options']):
            print(f"   {chr(65 + j)}. {option}")
        print(f"   Correct: {q['correct_answer']}")

    while True:
        action = input("\nChoose action: (E)dit, (D)elete, (C)ancel: ").upper()
        if action == 'C':
            return

        if action in ['E', 'D']:
            try:
                q_num = int(input("Enter question number: ")) - 1
                if 0 <= q_num < len(results):
                    manage_question(results[q_num], action)
                    return
                print("Invalid question number!")
            except ValueError:
                print("Invalid input!")


def manage_question(question, action):
    with open('data/questions.json', 'r') as f:
        all_questions = json.load(f)

    if action == 'E':
        print("\nEditing question:")
        new_q = input(f"Question [{question['question']}]: ").strip() or question['question']

        new_options = []
        for i, opt in enumerate(question['options']):
            new_opt = input(f"Option {chr(65 + i)} [{opt}]: ").strip()
            new_options.append(new_opt if new_opt else opt)

        new_correct = input(f"Correct answer [{question['correct_answer']}]: ").upper()
        if not new_correct or new_correct not in ['A', 'B', 'C', 'D']:
            new_correct = question['correct_answer']

        for q in all_questions:
            if q['question'] == question['question']:
                q['question'] = new_q
                q['options'] = new_options
                q['correct_answer'] = new_correct
                break

        print("Question updated!")

    elif action == 'D':
        confirm = input("Are you sure you want to delete? (y/n): ").lower()
        if confirm == 'y':
            all_questions = [q for q in all_questions if q['question'] != question['question']]
            print("Question deleted!")

    with open('data/questions.json', 'w') as f:
        json.dump(all_questions, f)
