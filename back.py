from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# -----------------------------
# DATABASE CONNECTION FUNCTION
# -----------------------------
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="YOUR_PASSWORD",   # <-- CHANGE THIS
            database="campus_jobs",
            port=3306
        )

        print("✅ MySQL Connected")
        return connection

    except mysql.connector.Error as err:
        print("❌ Database Connection Failed:", err)
        return None


# -----------------------------
# SAVE STUDENT DATA
# -----------------------------
@app.route("/search", methods=["POST"])
def search_job():

    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database not connected"}), 500

    cursor = db.cursor()

    data = request.json

    name = data.get("name")
    timing = data.get("timing")
    job_type = data.get("job_type")

    sql = """
        INSERT INTO students(name, timing, job_type)
        VALUES (%s,%s,%s)
    """

    cursor.execute(sql, (name, timing, job_type))
    db.commit()

    cursor.close()
    db.close()

    return jsonify({"message": "Student preference saved"})


# -----------------------------
# GET JOBS
# -----------------------------
@app.route("/jobs", methods=["GET"])
def get_jobs():

    db = get_db_connection()
    if db is None:
        return jsonify({"error": "Database not connected"}), 500

    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    cursor.close()
    db.close()

    return jsonify(jobs)


# -----------------------------
# APPLY JOB
# -----------------------------
@app.route("/apply/<int:job_id>", methods=["POST"])
def apply(job_id):

    return jsonify({
        "message": f"Applied successfully for Job ID {job_id}"
    })


# -----------------------------
# RUN SERVER
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)