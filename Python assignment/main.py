import json
import os
import admin
import quiz


def main_menu():
    print("\n===== SMART ONLINE QUIZ SYSTEM =====")
    print("1. Take Quiz")
    print("2. View Leaderboard")
    print("3. Admin Login")
    print("4. Exit")

    choice = input("Enter choice: ")
    return choice


def main():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists('data/questions.json'):
        with open('data/questions.json', 'w') as f:
            json.dump([], f)

    if not os.path.exists('data/leaderboard.json'):
        with open('data/leaderboard.json', 'w') as f:
            json.dump([], f)

    while True:
        choice = main_menu()

        if choice == '1':
            username = input("Enter your name: ")
            questions = quiz.load_questions()
            if not questions:
                print("No questions available!")
                continue
            user_answers, time_taken = quiz.take_quiz(questions)
            score = quiz.calculate_score(questions, user_answers)
            quiz.save_result(username, score, time_taken)

        elif choice == '2':
            quiz.view_leaderboard()

        elif choice == '3':
            admin.admin_menu()

        elif choice == '4':
            print("Exiting SOQS. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()