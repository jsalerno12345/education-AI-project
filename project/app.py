from flask import Flask, request, render_template, jsonify
import sqlite3
from sympy import sympify, solve, diff, integrate

app = Flask(__name__)

def init_db():
    # Initialize the database and create necessary tables if they don't exist
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem TEXT NOT NULL,
            solution TEXT,
            ai_solution TEXT,
            correct BOOLEAN,
            submitted_by TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET"])
def index():
    # Render the main page
    return render_template("index.html")

@app.route("/submit_problem", methods=["POST"])
def submit_problem():
    problem = request.form.get("problem")
    solution = request.form.get("solution")

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (problem, solution) VALUES (?, ?)", (problem, solution)
    )
    conn.commit()
    conn.close()

    return "Problem submitted successfully!"

@app.route("/solve_problem", methods=["POST"])
def solve_problem():
    problem = request.form.get("problem")

    try:
        # Use sympy to parse and solve the problem
        sympy_problem = sympify(problem)
        if "diff" in problem:
            result = str(diff(sympy_problem))
        elif "integrate" in problem:
            result = str(integrate(sympy_problem))
        else:
            result = str(solve(sympy_problem))
    except Exception as e:
        result = f"Error solving problem: {e}"

    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO problems (problem, ai_solution) VALUES (?, ?)", (problem, result)
    )
    conn.commit()
    conn.close()

    return jsonify({"solution": result})

@app.route("/grade", methods=["GET"])
def grade():
    # Fetch all problems and their solutions for grading
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute("SELECT id, problem, solution, ai_solution FROM problems")
    rows = cursor.fetchall()
    conn.close()

    graded_results = []

    for row in rows:
        problem_id, problem, solution, ai_solution = row
        correct = str(solution).strip() == str(ai_solution).strip()

        graded_results.append({
            "problem_id": problem_id,
            "problem": problem,
            "solution": solution,
            "ai_solution": ai_solution,
            "correct": correct
        })

    return jsonify(graded_results)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
