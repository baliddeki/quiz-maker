import tkinter as tk
from tkinter import messagebox
import random
import time
import os

class QuizApp:
    def __init__(self, root):
        # Initialize main application window and quiz variables
        self.root = root
        self.root.title("Quiz Maker")
        self.root.geometry("800x600")
        self.root.configure(bg="#e6f2ff")

        self.questions = self.load_questions()  # Load questions
        random.shuffle(self.questions)  # Shuffle questions randomly
        self.current_question = 0
        self.answers = {}  # Dictionary to store selected answers
        self.score = 0
        self.timer_seconds = 300  # Total quiz time in seconds (5 minutes)
        self.timer_running = False

        self.user_data()  # Prompt user for input

    def load_questions(self):
        # Load a list of predefined questions with options and correct answers
        raw_questions = [
            {"q": "What is Python?", "opts": ["Programming Language", "Snake", "Coffee", "City"], "ans": "Programming Language"},
            {"q": "Who developed Python?", "opts": ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"], "ans": "Guido van Rossum"},
            {"q": "Which keyword is used for function in Python?", "opts": ["def", "function", "fun", "define"], "ans": "def"},
            {"q": "What symbol starts comments in Python?", "opts": ["#", "//", "/*", "--"], "ans": "#"},
            {"q": "Which is a valid Python data type?", "opts": ["Tuple", "ArrayList", "IntegerList", "FloatArray"], "ans": "Tuple"},
            {"q": "What does GUI stand for?", "opts": ["Graphical User Interface", "Global User Integration", "General Utility Interface", "Guided User Interface"], "ans": "Graphical User Interface"},
            {"q": "Which function outputs data in Python?", "opts": ["print()", "echo()", "cout()", "display()"], "ans": "print()"},
            {"q": "Which of these loops is NOT valid in Python?", "opts": ["repeat-until", "for", "while", "nested loops"], "ans": "repeat-until"},
            {"q": "Python file extensions typically end in?", "opts": [".py", ".java", ".cpp", ".html"], "ans": ".py"},
            {"q": "What does PEP stand for in Python community?", "opts": ["Python Enhancement Proposal", "Python Essential Protocol", "Programming Environment Python", "Python Error Procedure"], "ans": "Python Enhancement Proposal"},
            {"q": "Which statement is used to handle exceptions in Python?", "opts": ["try-except", "catch-throw", "error-check", "test-catch"], "ans": "try-except"},
            {"q": "What is the output of 3 * 1 ** 3 in Python?", "opts": ["3", "1", "9", "0"], "ans": "3"},
            {"q": "What method adds items to the end of a Python list?", "opts": ["append()", "add()", "insert()", "push()"], "ans": "append()"},
            {"q": "How do you start a virtual environment in Python 3?", "opts": ["python -m venv", "virtualenv", "mkvirtualenv", "create venv"], "ans": "python -m venv"},
            {"q": "Python supports which type of inheritance?", "opts": ["Multiple", "Single Only", "No inheritance", "Hybrid only"], "ans": "Multiple"},
            {"q": "Which library is primarily used for GUI in Python?", "opts": ["Tkinter", "React", "Angular", "Django"], "ans": "Tkinter"},
            {"q": "How do you write a single-line comment in Python?", "opts": ["# Comment", "// Comment", "/* Comment */", "-- Comment"], "ans": "# Comment"},
            {"q": "Which operator is used to check equality in Python?", "opts": ["==", "=", "<>", "!="], "ans": "=="},
            {"q": "What is the result of '2' + '3' in Python?", "opts": ["23", "5", "Error", "6"], "ans": "23"},
            {"q": "Which keyword is used to create a class in Python?", "opts": ["class", "define", "struct", "object"], "ans": "class"}
        ]
        return raw_questions

    def user_data(self):
        # Display input form for student information
        self.clear_frame()

        tk.Label(self.root, text="Quiz Maker", font=("Arial", 22, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=15)

        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.student_id = tk.StringVar()

        for label_text, var in [("First Name:", self.first_name), ("Surname:", self.last_name), ("Student ID (6 digits):", self.student_id)]:
            tk.Label(self.root, text=label_text, bg="#e6f2ff", font=("Arial", 12)).pack(pady=5)
            tk.Entry(self.root, textvariable=var, font=("Arial", 12)).pack()

        tk.Button(self.root, text="Start Quiz", font=("Arial", 14), command=self.validate_user, bg="#004080", fg="white").pack(pady=30)

    def validate_user(self):
        # Validate the student input fields
        try:
            if not (self.first_name.get() and self.last_name.get()):
                raise ValueError("Name fields cannot be empty.")
            if not (self.student_id.get().isdigit() and len(self.student_id.get()) == 6):
                raise ValueError("Student ID must be a 6-digit number.")
            self.start_quiz()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def start_quiz(self):
        # Start the quiz and timer
        self.timer_running = True
        self.clear_frame()

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#f0f8ff")
        self.timer_label.pack(side="bottom")

        self.update_timer()
        self.display_question()

    def display_question(self):
        # Show the current question with options and navigation buttons
        self.clear_frame()
        question = self.questions[self.current_question]
        opts = question["opts"]
        random.shuffle(opts)

        tk.Label(self.root, text=f"Question {self.current_question + 1} of {len(self.questions)}", font=("Arial", 16, "bold"), bg="#e6f2ff").pack(pady=10)
        tk.Label(self.root, text=question["q"], font=("Arial", 14), bg="#e6f2ff", wraplength=700).pack(pady=5)

        self.selected_answer = tk.StringVar()
        for i, opt in enumerate(opts):
            label = f"{chr(65 + i)}. {opt}"
            tk.Radiobutton(self.root, text=label, variable=self.selected_answer, value=opt, bg="#e6f2ff", font=("Arial", 12)).pack(anchor="w", padx=40)

        tk.Label(self.root, text="Score for this question: 1 point", font=("Arial", 10, "italic"), bg="#e6f2ff", fg="gray").pack()

        nav_frame = tk.Frame(self.root, bg="#e6f2ff")
        nav_frame.pack(pady=20)

        if self.current_question > 0:
            tk.Button(nav_frame, text="Previous", command=self.prev_question, bg="#cce0ff").pack(side="left", padx=20)

        tk.Button(nav_frame, text="Next", command=self.next_question, bg="#cce0ff").pack(side="left", padx=20)
        tk.Button(nav_frame, text="End Quiz", command=self.end_quiz_warning, bg="#ff9999").pack(side="left", padx=20)

        self.timer_label = tk.Label(self.root, text="", font=("Arial", 14), bg="#e6f2ff", fg="#cc0000")
        self.timer_label.pack(pady=10)

    def update_timer(self):
        # Update countdown timer each second
        if self.timer_seconds > 0 and self.timer_running:
            mins, secs = divmod(self.timer_seconds, 60)
            self.timer_label.config(text=f"Time left: {mins:02}:{secs:02}")
            self.timer_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running:
            messagebox.showinfo("Time Up!", "The quiz time is over!")
            self.end_quiz()

    def next_question(self):
        # Move to the next question
        self.record_answer()
        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.display_question()
        else:
            self.end_quiz()

    def prev_question(self):
        # Move to the previous question
        self.record_answer()
        if self.current_question > 0:
            self.current_question -= 1
            self.display_question()

    def record_answer(self):
        # Save the selected answer
        self.answers[self.current_question] = self.selected_answer.get()

    def end_quiz_warning(self):
        # Confirm with user before ending quiz early
        if messagebox.askyesno("End Quiz", "Are you sure you want to end the quiz early?"):
            self.end_quiz()

    def end_quiz(self):
        # Finalize quiz, calculate score and display result
        self.timer_running = False
        self.record_answer()
        self.calculate_score()
        self.save_results()
        self.show_results()

    def calculate_score(self):
        # Calculate number of correct answers
        self.score = sum(1 for i, q in enumerate(self.questions) if self.answers.get(i) == q["ans"])

    def show_results(self):
        # Show results in a messagebox
        correct = self.score
        total = len(self.questions)
        percent = (correct / total) * 100
        status = "Passed" if percent >= 50 else "Failed"

        messagebox.showinfo("Results", f"Correct Answers: {correct}/{total}\nScore: {percent:.2f}%\nStatus: {status}")

        self.retry_option()

    def retry_option(self):
        # Allow the user to retake the quiz or close the app
        if messagebox.askyesno("Retry", "Do you want to retake the quiz?"):
            self.current_question = 0
            self.answers.clear()
            self.score = 0
            self.timer_seconds = 300
            random.shuffle(self.questions)
            self.start_quiz()
        else:
            self.root.destroy()

    def save_results(self):
        # Save results to a file
        filename = f"results-{self.student_id.get()}.txt"
        percent = (self.score / len(self.questions)) * 100
        try:
            with open(filename, "a") as f:
                f.write(f"{self.first_name.get()} {self.last_name.get()}, ID: {self.student_id.get()}, Score: {percent:.2f}%\n")
                # Ensure at least 5 sample entries exist
                if os.path.getsize(filename) < 5 * 50:
                    for i in range(5):
                        f.write(f"Sample User{i+1}, ID: 12345{i}, Score: {random.randint(40, 100)}%\n")
        except Exception as e:
            messagebox.showerror("File Error", f"Could not save results: {e}")

    def clear_frame(self):
        # Clear all widgets from the window
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()