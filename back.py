from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # allow frontend connection

DATABASE = "campus_jobs.db"

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # return results as dictionary
    return conn


# -----------------------------
# CREATE TABLES (Auto-create if not exists)
# -----------------------------
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            timing TEXT,
            job_type TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            location TEXT,
            timing TEXT,
            job_type TEXT,
            pay TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            student_name TEXT
        )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# SAVE STUDENT + RETURN MATCHED JOBS
# -----------------------------
@app.route("/search", methods=["POST"])
def search_job():

    conn = get_db_connection()
    cursor = conn.cursor()

    data = request.json
    name = data.get("name")
    timing = data.get("timing")
    job_type = data.get("job_type")
    print("vars", name, timing, job_type)

    # Save student preference
    cursor.execute(
        "INSERT INTO students(name, timing, job_type) VALUES (?, ?, ?)",
        (name, timing, job_type)
    )
    conn.commit()

    # Fetch matching jobs
    cursor.execute(
        "SELECT * FROM jobs WHERE timing=? AND job_type=?",
        (timing, job_type)
    )

    jobs = cursor.fetchall()
    job_list = [dict(job) for job in jobs]

    conn.close()
    print(job_list)

    return jsonify(job_list)


# -----------------------------
# APPLY JOB
# -----------------------------
@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    data = request.json
    name = data.get("name")

    cursor.execute(
        "INSERT INTO applications(job_id, student_name) VALUES (?, ?)",
        (job_id, name)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "Application successful"})


def seed_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    if count == 0:
        jobs = [
            ("Online Tutor","Work From Home","Morning","Online Work","₹6000-₹12000"),
            ("Cafe Assistant","Kakkanad","Afternoon","Store Assistant","₹8000-₹10000"),
            ("Content Writer","Remote","Flexible","Freelancing","₹5000-₹15000"),
            ("Library Assistant","Edappally","Day Shift","Teaching","₹7000-₹9000"),
            ("Kids Tuition Mentor","Aluva","Evening","Teaching","₹8000-₹14000"),
            ("Boutique Helper","Marine Drive","Day Only","Store Assistant","₹9000-₹11000")
        ]

        cursor.executemany("""
        INSERT INTO jobs(title, location, timing, job_type, pay)
        VALUES (?, ?, ?, ?, ?)
        """, jobs)

    conn.commit()
    conn.close()

@app.route("/jobs", methods=["GET"])
def get_all_jobs():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    conn.close()
    return jsonify([dict(job) for job in jobs])
# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    init_db()  # create tables automatically
    seed_jobs()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)