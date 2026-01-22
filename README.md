Introduction 

Overview of the system 
The Smart Online Quiz System (SOQS) is a command-line Python application designed to simulate a real-world quiz-taking experience in an educational context. To help students use Python to solve problems on a grand scale, it has been developed as a modular, team-based project. The system supports multiple-choice quizzes, provides real-time feedback so you can know how you did after taking each one and see this information displayed dynamically on a leaderboard. Included also is an administrative mode that one can use to manage quiz content. This takes the form of adding or deleting questions or sorting them by category.
Objective and motivation

The main characteristics of SOQS are as follows:

•	Randomized question selection from a structured JSON database
•	Real-time scoring with qualitative feedback in the form of simple, correct, good and quick messages on screen
•	Use CSV for log file storage and management, working on-line feature(s)
•	There is only an administrator able to enter or change questions
•	Robust user inputs error-handling and verification of the answers in SOQS.

As a project which aspires to provide a complete monolith application environment, it therefore needs to have through programming the requisite skills including file I/O, control structure statements, data structures such as lists and dictionaries, as well as modular function design.

The motivation to develop SOQS was for:
1.	Educational Benefits: To simulate a practical online quiz system that can be adapted for classroom use, peer competitions, or self-assessment.
2.	Skill Development: To encourage collaboration among students while improving proficiency in key programming areas, such as modular development, debugging, testing, and persistent storage.

Furthermore, the initiative intends to improve soft skills like teamwork, problem solving, communication, and documentation, which are essential for future academic or professional programming efforts.

System Design 

Description of modules and their purposes

1.	load_questions()

Purpose: To load quiz questions into the system from an external JSON file.

            Description:
•	Reads questions, options, and correct answers from a structured JSON file. 
•	Validates each entry to ensure it contains required fields:”question”, “options”, and “correct_answer”.
•	Handles file errors (example: missing or corrupted files).
•	Randomly selects 10 questions for each quiz attempt to keep quizzes dynamic and engaging.

2.	take_quiz()

            Purpose: To manage the user’s quiz session.

            Description:
•	Displays one question at a time along with its options (A/B/C/D).
•	Accepts and validates user input to prevent invalid entries.
•	Tracks user responses and identifies skipped or incorrect answers.
•	Optionally includes a countdown timer per question or for the entire quiz duration.

3.	calculate_score()

            Purpose: To evaluate the user's performance after completing the quiz.

            Description:
•	Compares the user's answers with the correct ones and calculates the total score.
•	Provides feedback summary (correct, incorrect, skipped).
•	Gives qualitative feedback (Excellent, Good, Fair, Needs Improvement) based on score percentage.
•	Displays incorrectly answered questions along with correct answers for user learning.

4.	save_result()

Purpose: To save the quiz results in a format that can be stored for a long time.

Description:
•	Saves the user's name, score, date, and time to a CSV or JSON file.
•	Ensures that results are stored consistently for leaderboard display.
•	Protects stored data from user-side manipulation.

5.	view_leaderboard()

Purpose: To display the quiz system’s top performers.

Description:
•	Displays the top 10 scores from the leaderboard in descending order.
•	Includes timestamps to differentiate duplicate names or scores.
•	Accessible to all users for motivation and transparency.

6.	add_question() (Admin Only)
Purpose: To allow the admin to add new questions to the quiz database.

Description:
•	Accepts input for question text, four options, and the correct answer.
•	Validates that each question has only one correct answer (A/B/C/D).
•	Checks for duplication to avoid redundant questions.
•	Accessible only via password-protected admin mode to prevent unauthorized use.

7. search_question() (Admin Only)

Purpose: To enable admins to find specific questions in the database.

Description:
•	Allows keyword-based search for questions.
•	Displays search results in a clear format for review.
•	Enables editing or deletion of specific questions after confirmation.
•	Ensures safe modifications of the quiz question database.


Diagram 1.1 File structure and flow diagrams

Screenshots of sample runs
 
Figure 1.1 View leaderboard sample run
 
Figure 1.2 Main and Quiz sample run
 
Figure 1.3 Entering the wrong admin password sample run
 
Figure 1.4 Search question sample run
 
Figure 1.5 Editing question’s options sample run

Testing and Results 
How the system was tested
Provide the actual parameters to test whether the results achieve the predicted results, and secondly, swap the wrong parameters to test the system error reporting effect has not appeared. In the admin design section, it is to test the mainstream functions such as adding topics, modifying topics, searching for topics, and checking whether the added topics have appeared in the JSON file. Test in the player system can view the correct question. As well as answer the question after each player's name, answer the question score, and answer the question time has not been recorded in the JSON file.

Screenshots of test outcomes/Example test cases
 
Figure 1.6 Entering wrong admin password with 3 try’s until reset password
 
Figure 1.7 Entering wrong security question until fail to login into admin
 
Figure 1.8 Entering the wrong question number
 
Figure 1.9 Entering the invalid question and options

Challenges Faced 

A. Technical Issues
1. File Not Found or Corrupted Data
•	Issue:
The program would previously crash if questions.json, leaderboard.json, or admin_config.json were missing, renamed, or contained malformed JSON.
•	Solution:
Improved by using try-except handling in file-loading functions (e.g., quiz.load_questions(), config.get_config(), quiz.save_result()).
o	On startup, main.py automatically creates default files (questions.json, leaderboard.json) if they do not already exist.
o	The default configuration is used, if admin_config.json is not present. 
o	Invalid JSON results in safe defaults instead of crashes.

2. Input Validation Errors
•	Issue:
When taking the quiz users might enter invalid answers (lowercase letters, empty input, random strings).
•	Solution:
To ensure that only valid options (A, B, C, and D) are selected, the reusable utils. validate_input() function was incorporated into quiz.take_quiz().
o	When case-insensitive mode is used, input is automatically converted to uppercase 
o	Until a valid option is entered, users are prompted.

3. Leaderboard Tampering or Duplicate Entries
•	Issue:
The leaderboard JSON could be manually altered to cheat, and multiple entries with the same username caused confusion. 
•	Solution:
o	To differentiate identical usernames, a timestamp is now included in every leaderboard entry. 
o	Leaderboard writing is restricted to the quiz.save_result() function.
o	The leaderboard file is loaded with error handling to prevent crashes from manual edits.

4. Question Randomization Without Repetition
•	Issue:
In a single quiz, the same question could appear multiple times.
•	Solution:
To ensure unique, non-repeating questions per quiz session, replaced random.choice() with random.sample() in quiz.load_questions().

5. Admin Mode Security
•	Problem:
There were no restrictions on who could access admin functions.
•	Solution:
So, we added a password-protected admin login to admin.admin_menu().
o	Passwords are securely hashed using hashlib in config.hash_value().
o	Security questions are stored in admin_config.json.
o	Password rules enforced in config.validate_password() (minimum length, at least one digit, one uppercase letter).

B. Team-Related Issues
1.	Issue: Code Integration Conflicts
o	Problem: Runtime errors happens when combining modules, inconsistent data handling and function naming conflicts.
o	Solution: Followed consistent naming conventions and modular design principles. Used regular team syncs and pair programming sessions to align on function interfaces and data formats.
2.	Issue: Communication Gaps
o	Problem: Delays in updates and changes that affected team coordination.
o	Solution: Set up a dedicated WhatsApp group for instant communication and used Google Docs for live documentation and status updates.
3.	Issue: Testing and Bug Tracking
o	Problem: Until the final integration some bugs remained unnoticed.
o	Solution: Assigned one member as a "tester" to perform integration testing before final submission.
4.	Issue: Different Skill Levels
o	Problem: Some members were new to Python or JSON handling.
o	Solution: Conducted short peer tutorial sessions to upskill teammates and shared learning resources. Encouraged pair coding to help slower learners keep up.

Conclusion and Reflection 

Lessons learned 
First and foremost, throughout this assignment we learned practical Python programming skills like the core concepts of the application such as data structures, file handling using JSON, control flow like loops and conditionals, and functions and modular programming. Moreover, writing clean, reusable and well-commented code. Secondly, we learned how to anticipate and manage user input errors, handling file read/write exceptions such as missing files and wrong format, and building a robust system that doesn’t crash on unexpected input. Thirdly, we understand how to divide responsibilities in a group project, and practicing effective communication and coordination. Fourth, we understand how to store and retrieve data between program runs, thinking algorithmically to implement logic scoring and ranking, and using structured formats like JSON for real world data handling.

Suggestions for future improvements
1. Upgrading from a command line interface to a user-friendly Graphical User Interface (GUI).
2. Allowing users to select quiz-based categories. Example, Math, Science, and Computer Science.
3. Adding difficulty levels (Easy, Medium, Hard) for more personalized quizzes.
4. Allow users to participate in multiplayer mode to compete against each other in real time based challenges.
5. Implementing a login and registration system for users and admins.
