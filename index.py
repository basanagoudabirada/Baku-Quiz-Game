import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib
import pandas as pd

# ---------- DATABASE SETUP ----------
conn = sqlite3.connect("quiz_game.db")
cursor = conn.cursor()

# ------FETCHING DATA-----
print(conn)
cursor=conn.cursor()
cursor.execute("select * from users")
print(pd.DataFrame(cursor.fetchall(),columns=["username","password","is_admin"]))


cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)
''')
#cursor.execute('''
#   ALTER TABLE users ADD COLUMN is_admin INTEGER DEFAULT 0
#''')

#cursor.execute("UPDATE users SET is_admin = 1 WHERE username = ?", ("baku",))


cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    topic TEXT,
    score INTEGER,
    FOREIGN KEY(username) REFERENCES users(username)
)
''')
#cursor.execute('''
#   ALTER TABLE scores RENAME TO old_scores
#''')
conn.commit()

# ---------- QUIZ DATA ----------
quiz_data = {
    "AI": [
        {
            "question": "The different types of machine learning?         1 Marks",
            "options": ["Supervised", "Unsupervised", "Reinforcement", "All of the above"],
            "answer": "All of the above"
        },
        {
            "question": "The measure of performance of an AI agent is measured using ?           1 Marks",
            "options": ["Learning agent", "Changing agent", "Both 1 and 2", "None of the above"],
            "answer": "Learning agent"
        },
        {
            "question": "The process of breaking an image into parts is called?         1 Marks",
            "options": ["Smoothing", "Segmentation", "Processing", "Break Down"],
            "answer": "Segmentation"
        },
        {
            "question": "The process of making 2 logical expression look identical called?       1 Marks",
            "options": ["Unification", "Lifting", "Concatenation", "None of the above"],
            "answer": "Unification"
        },
        {
            "question": "What is the work of Task Environment and Rational Agents?           1 Marks",
            "options": ["Problem & Solution", "Solution & Problem", "Observation & Problem", "Observation & Solution"],
            "answer": "Problem & Solution"
        }
    ],
    "Blockchain": [
        {
            "question": "What is BlockChain?       1 Marks",
            "options": ["Type of Database", "Decentralized Ledger", "Networking Protocal", "Centralised Database"],
            "answer": "Decentralized Ledger"
        },
        {
            "question": "What is first block of a blockchain called?        1 Marks",
            "options": ["Root Block", "Genesis Block", "Origin Block", "Seed Block"],
            "answer": "Genesis Block"
        },
        {
            "question": "Who introduced Blockchain Technology?        1 Marks",
            "options": ["Basanagouda", "Satoshi Nakamoto", "Kirankumar", "Robin Hood"],
            "answer": "Satoshi Nakamoto"
        },
        {
            "question": "Which of the following is key feature of Blockchain?       1 Marks",
            "options": ["Dependence on Single Server", "High Centralization", "Insecure Data Transfer", "Immutability"],
            "answer": "Immutability"
        },
{
            "question": "Which is the first cryptocurrency to use Blockchain Technology?      1 Marks",
            "options": ["Bitcoin", "Ripple", "Litecoin", "Rupee"],
            "answer": "Bitcoin"
        },
    ],
    "Big Data": [
        {
            "question": "Which of the following tool used in Big Data?      1 Marks",
            "options": ["JDK", "Apache Hadoop", "Eclipse", "MYSQL"],
            "answer": "Apache Hadoop"
        },
        {
            "question": "Identify the slave node among the following?      1 Marks",
            "options": ["Job node", "Task node", "Data node", "Name node"],
            "answer": "Data node"
        },
{
            "question": "Which term is used to define multidimensional model of the data were house?           1 Marks",
            "options": ["Data Cube", "Table", "Tree", "Data Structure"],
            "answer": "Data Cube"
        },
{
            "question": "Mapper class is?     1 Marks",
            "options": ["Final", "Abstract type", "Static type", "Generic type"],
            "answer": "Generic type"
        },
{
            "question": "Identify whether true or false:Qubole is a big data tool?     1 Marks",
            "options": ["True", "False"],
            "answer": "True"
        }
    ],
    "DBMS": [
        {
            "question": "Which of the following is type of attribute in DBMS?      1 Marks",
            "options": ["All of the below", "Complex attribute", "Composite attribute", "Simple attribute"],
            "answer": "All of the below"
        },
        {
            "question": "What does 'TRUNCATE' operation?     1 Marks",
            "options": ["Delete specific row", "Modify row", "Add rows", "Delete all rows"],
            "answer": "Delete all rows"
        },
        {
            "question": "Which of the following is not function of DBMS?      1 Marks",
            "options": ["Dividing", "Manipulating", "Sharing", "Construction"],
            "answer": "Dividing"
        },
        {
            "question": "Which is the suitable operation for TCL(transactional control langauge)?    1 Marks",
            "options": ["UNIQUE", "COMMIT", "SELECT", "UPDATE"],
            "answer": "COMMIT"
        },
        {
            "question": "SQL Stands for?     1 Marks",
            "options": ["Standard Query Langauge", "Simple Quantum Life", "Structured Query Langauge",
                        "Strong Quality Langauge"],
            "answer": "Structured Query Language"
        }
    ],
    "Cyber Security": [
        {
            "question": "Who is the father of computer security?      1 Marks",
            "options": ["August Kerckhoffs", "Charles", "Bob Thomas", "Robert"],
            "answer": "August Kerckhoffs"
        },
        {
            "question": "Which of the following is not a cybercrime?      1 Marks",
            "options": ["Malware", "Man in Middle", "Denial of service", "AES"],
            "answer": "AES"
        },
{
            "question": "Which of the following is not a an advantage of cyber security?     1 Marks",
            "options": ["Protects systems", "Gives privacy to users", "Makes the system slower", "Minimizes computer crashes"],
            "answer": "Makes the system slower"
        },
{
            "question": "'CyberSpace' was coined by_____?      1 Marks",
            "options": ["Richard smit", "William Gibson", "Charles", "Jupiter"],
            "answer": "William Gibson"
        },
{
            "question": "Which of the following act violates cyber security?       1 Marks",
            "options": ["Exploit", "Threat", "Attack", "Vulnerability"],
            "answer": "Attack"
        }
    ]
}

# ---------- MAIN APP ----------
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Game")
        self.root.geometry("400x400")
        self.logged_in_user = None
        self.selected_topic = None
        self.question_index = 0
        self.score = 0

        self.login_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ---------- Login/Register ----------
    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=('Arial', 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.login_username = tk.Entry(self.root)
        self.login_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.login_password = tk.Entry(self.root, show='*')
        self.login_password.pack()

        tk.Button(self.root, text="Login", command=self.login_user).pack(pady=5)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()


    def register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=('Arial', 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        self.reg_username = tk.Entry(self.root)
        self.reg_username.pack()

        tk.Label(self.root, text="Password").pack()
        self.reg_password = tk.Entry(self.root, show='*')
        self.reg_password.pack()

        tk.Button(self.root, text="Register", command=self.register_user).pack(pady=5)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def register_user(self):
        username = self.reg_username.get()
        password = self.reg_password.get()

        if username == "" or password == "":
            messagebox.showwarning("Warning", "Fields cannot be empty")
            return

        hashed = hashlib.sha256(password.encode()).hexdigest()

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            self.login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def login_user(self):
        username = self.login_username.get()
        password = self.login_password.get()
        hashed = hashlib.sha256(password.encode()).hexdigest()

        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed))
        user = cursor.fetchone()

        if user:
            self.logged_in_user = username
            messagebox.showinfo("Success", "Successful login")
            self.topic_selection()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    # ---------- Topic and Quiz ----------
    def topic_selection(self):
        self.clear_screen()
        tk.Label(self.root, text=f"Welcome {self.logged_in_user}!", font=('Arial', 16)).pack(pady=10)

        tk.Label(self.root, text="Select a Quiz Topic", font=('Arial', 14)).pack(pady=10)

        for topic in quiz_data.keys():
            tk.Button(self.root, text=topic, width=20,
                      command=lambda t=topic: self.start_quiz(t)).pack(pady=5)

        tk.Button(self.root, text="View History", command=self.view_history).pack(pady=10)

        # Only show Admin Panel if user is admin
        cursor.execute("SELECT is_admin FROM users WHERE username = ?", (self.logged_in_user,))
        is_admin = cursor.fetchone()[0]
        if is_admin:
            tk.Button(self.root, text="Admin Panel", command=self.admin_panel, bg="orange").pack(pady=10)

        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    def start_quiz(self, topic):
        self.selected_topic = topic
        self.question_index = 0
        self.score = 0
        self.show_question()
        self.percentage=0

    def show_question(self):
        self.clear_screen()
        questions = quiz_data[self.selected_topic]
        if self.question_index < len(questions):
            q_data = questions[self.question_index]
            tk.Label(self.root, text=f"{self.selected_topic} - Q{self.question_index + 1}:", font=('Arial', 12)).pack(pady=5)
            tk.Label(self.root, text=q_data['question'], wraplength=350).pack(pady=5)

            self.var = tk.StringVar()
            for option in q_data['options']:
                tk.Radiobutton(self.root, text=option, variable=self.var, value=option).pack(anchor='w')
            tk.Button(self.root, text="Next", command=self.next_question).pack(pady=10)
        else:
            self.save_score()
            self.show_result()

    def next_question(self):
        selected = self.var.get()
        if not selected:
            messagebox.showwarning("No selection", "Please choose an option!")
            return

        correct_answer = quiz_data[self.selected_topic][self.question_index]['answer']
        if selected == correct_answer:
            self.score += 1

        self.question_index += 1
        self.show_question()

    def show_result(self):
        self.clear_screen()
        total = len(quiz_data[self.selected_topic])
        self.percentage= self.score/total*100
        tk.Label(self.root, text=f"{self.selected_topic} Quiz Complete!", font=('Arial', 16)).pack(pady=10)
        tk.Label(self.root, text=f"{self.logged_in_user}, Your Score is {self.score}/{total}",font=('Arial',13)).pack(pady=10)
        tk.Label(self.root,text=f" You percentage is {self.percentage}%", font=('Arial',13)).pack(pady=10)
        if self.selected_topic=="AI":
            tk.Label(self.root,text="Q1. The different type of machine learning?").pack(pady=10)
            tk.Label(self.root,text="Answer: All of the Above").pack(pady=10)

            tk.Label(self.root,text="Q2. The measure of performance of an AI Agent is measured using?").pack(pady=10)
            tk.Label(self.root,text="Answer: Learning agent").pack(pady=10)

            tk.Label(self.root,text="Q3. The process of breaking an image into parts is called?").pack(pady=10)
            tk.Label(self.root,text="Answer: Segmentation").pack(pady=10)

            tk.Label(self.root,text="Q4. The process of making 2 logical expression look identical is called?").pack(pady=10)
            tk.Label(self.root,text="Answer: Unification").pack(pady=10)

            tk.Label(self.root,text="Q5. What is the work of Task Environment and Rational Agents?").pack(pady=10)
            tk.Label(self.root,text="Answer: Problem & Solution").pack(pady=10)

        if self.selected_topic == "Blockchain":
            tk.Label(self.root, text="Q1. What is Blockchain?").pack(pady=10)
            tk.Label(self.root, text="Answer: Decentralized Ledger").pack(pady=10)

            tk.Label(self.root, text="Q2. What is the first block of Blockchain called?").pack(pady=10)
            tk.Label(self.root, text="Answer: Genesis Block").pack(pady=10)

            tk.Label(self.root, text="Q3. Who introduced Blockchain Technology?").pack(pady=10)
            tk.Label(self.root, text="Answer: Satoshi Nakamoto").pack(pady=10)

            tk.Label(self.root, text="Q4. Which of the following is key feature of Blockchain?").pack(pady=10)
            tk.Label(self.root, text="Answer: Immutability").pack(pady=10)

            tk.Label(self.root, text="Q5. Which is the first cryptocurrency to use Blockchain Technology?").pack(pady=10)
            tk.Label(self.root, text="Answer: Bitcoin").pack(pady=10)

        if self.selected_topic == "Big Data":
            tk.Label(self.root, text="Q1. Which of the following tool used in Big Data?").pack(pady=10)
            tk.Label(self.root, text="Answer: Apache Hadoop").pack(pady=10)

            tk.Label(self.root, text="Q2. Identify the slave node among the following?").pack(pady=10)
            tk.Label(self.root, text="Answer: Data node").pack(pady=10)

            tk.Label(self.root, text="Q3. Which term is used to define multidimensional model of the data were house?").pack(pady=10)
            tk.Label(self.root, text="Answer: Data Cube").pack(pady=10)

            tk.Label(self.root, text="Q4. Mapper class is ?").pack(pady=10)
            tk.Label(self.root, text="Answer: Generic type").pack(pady=10)

            tk.Label(self.root, text="Q5. Identify whether true or false:Qubole is a big data tool?").pack(pady=10)
            tk.Label(self.root, text="Answer: True").pack(pady=10)

        if self.selected_topic == "DBMS":
            tk.Label(self.root, text="Q1. Which of the following is type of attribute in DBMS?").pack(pady=10)
            tk.Label(self.root, text="Answer: All of the Above").pack(pady=10)

            tk.Label(self.root, text="Q2. What does 'TRUNCATE' operation ?").pack(pady=10)
            tk.Label(self.root, text="Answer: Delete all rows").pack(pady=10)

            tk.Label(self.root, text="Q3. Which of the following is not function of DBMS?").pack(pady=10)
            tk.Label(self.root, text="Answer: Dividing").pack(pady=10)

            tk.Label(self.root,text="Q4. Which is the suitable operation for TCL(transactional control langauge)?").pack(pady=10)
            tk.Label(self.root, text="Answer: COMMIT").pack(pady=10)

            tk.Label(self.root, text="Q5.SQL Stands for ?").pack(pady=10)
            tk.Label(self.root, text="Answer: Structured Query Langauge").pack(pady=10)

        if self.selected_topic == "Cyber Security":
            tk.Label(self.root, text="Q1. Who is the father of computer security?").pack(pady=10)
            tk.Label(self.root, text="Answer: August Kerckhoffs").pack(pady=10)

            tk.Label(self.root, text="Q2. Which of the following is not a cybercrime?").pack(pady=10)
            tk.Label(self.root, text="Answer: AES").pack(pady=10)

            tk.Label(self.root, text="Q3. Which of the following is not a an advantage of cyber security?").pack(pady=10)
            tk.Label(self.root, text="Answer: Makes the system slower").pack(pady=10)

            tk.Label(self.root, text="Q4. 'CyberSpace' was coined by_____?").pack(pady=10)
            tk.Label(self.root, text="Answer: William Gibson").pack(pady=10)

            tk.Label(self.root, text="Q5. Which of the following act violates cyber security?").pack(pady=10)
            tk.Label(self.root, text="Answer: Attacks").pack(pady=10)

        tk.Button(self.root, text="Choose Another Topic", command=self.topic_selection).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack()

    def save_score(self):
        cursor.execute("INSERT INTO scores (username, topic, score) VALUES (?, ?, ?)",
                       (self.logged_in_user, self.selected_topic, self.score))
        conn.commit()

    # ---------- Admin Panel ----------
    def admin_panel(self):
        self.clear_screen()
        tk.Label(self.root, text="Admin Panel", font=('Arial', 16), fg="blue").pack(pady=10)

        # Fetch all user quiz records
        cursor.execute("SELECT id, username, topic, score FROM scores ORDER BY username")
        records = cursor.fetchall()

        if not records:
            tk.Label(self.root, text="No quiz records found.", font=('Arial', 12)).pack(pady=10)
        else:
            for record_id, user, topic, score in records:
                percent = round((score / 5) * 100)
                frame = tk.Frame(self.root)
                frame.pack(pady=2)

                info = f"User: {user} | Topic: {topic} | Score: {score}/5 | {percent}%"
                tk.Label(frame, text=info, font=('Arial', 10)).pack(side=tk.LEFT)

                tk.Button(frame, text="Delete", fg="white", bg="red",
                          command=lambda r_id=record_id: self.delete_user_history(r_id)).pack(side=tk.RIGHT, padx=10)

        tk.Button(self.root, text="Back", command=self.topic_selection).pack(pady=10)

    def delete_user_history(self, record_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this quiz history?")
        if confirm:
            cursor.execute("DELETE FROM scores WHERE id = ?", (record_id,))
            conn.commit()
            messagebox.showinfo("Deleted", "Quiz history deleted successfully.")
            self.admin_panel()

    def delete_history(self):
        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete all your quiz history?")
        if confirm:
            cursor.execute("DELETE FROM scores WHERE username = ?", (self.logged_in_user,))
            conn.commit()
            messagebox.showinfo("Deleted", "Your quiz history has been deleted.")
            self.view_history()  # Refresh the screen

    def view_history(self):
        self.clear_screen()
        tk.Label(self.root, text="Quiz History", font=('Arial', 16)).pack(pady=10)

        cursor.execute("SELECT topic, score FROM scores WHERE username = ? ORDER BY rowid DESC", (self.logged_in_user,))
        history = cursor.fetchall()

        if not history:
            tk.Label(self.root, text="No quiz history found.", font=('Arial', 12)).pack(pady=10)
        else:
            for topic, score in history:
                percentage = round((score / 5) * 100)
                tk.Label(self.root, text=f"Topic: {topic} | Score: {score}/5 | {percentage}%",
                         font=('Arial', 12)).pack(pady=2)

            tk.Button(self.root, text="Delete History", command=self.delete_history, bg="red", fg="white").pack(pady=10)

        tk.Button(self.root, text="Back", command=self.topic_selection).pack(pady=10)


# ---------- RUN ----------
root = tk.Tk()
app = QuizApp(root)
root.mainloop()


