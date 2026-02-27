from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

DATABASE = "campus_jobs.db"


# -----------------------------
# DATABASE CONNECTION
# -----------------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# -----------------------------
# CREATE TABLES AUTOMATICALLY
# -----------------------------
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        timing TEXT,
        job_type TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        location TEXT,
        timing TEXT,
        pay TEXT,
        category TEXT,
        safety TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        job_id INTEGER
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# INSERT DEFAULT JOBS
# -----------------------------
def seed_jobs():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    if count == 0:
        jobs = [
            ("Online Tutor","Work From Home","Evening","₹6000-₹12000","Common","Verified"),
            ("Cafe Assistant","Kakkanad","Afternoon","₹8000-₹10000","Common","CCTV"),
            ("Content Writer","Remote","Flexible","₹5000-₹15000","Common","Online Verified"),
            ("Library Assistant","Edappally","Day Shift","₹7000-₹9000","Women Only","Safe"),
            ("Kids Tuition Mentor","Aluva","Evening","₹8000-₹14000","Women Only","Verified"),
            ("Boutique Helper","Marine Drive","Day Only","₹9000-₹11000","Women Only","Women Staff")
        ]

        cursor.executemany("""
        INSERT INTO jobs(title,location,timing,pay,category,safety)
        VALUES (?,?,?,?,?,?)
        """, jobs)

    conn.commit()
    conn.close()


# -----------------------------
# SAVE STUDENT SEARCH
# -----------------------------
@app.route("/search", methods=["POST"])
def search_job():

    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO students(name,timing,job_type)
        VALUES (?,?,?)
    """, (
        data["name"],
        data["timing"],
        data["job_type"]
    ))

    conn.commit()
    conn.close()

    return jsonify({"message": "Preference Saved"})


# -----------------------------
# GET JOBS
# -----------------------------
@app.route("/jobs", methods=["GET"])
def get_jobs():

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM jobs")
    jobs = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return jsonify(jobs)


# -----------------------------
# APPLY JOB
# -----------------------------
@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    data = request.json

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO applications(student_name,job_id)
        VALUES (?,?)
    """, (data["name"], job_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Applied Successfully"})


# -----------------------------
# START SERVER
# -----------------------------
if __name__ == "__main__":
    init_db()
    seed_jobs()
    app.run(debug=True)
    