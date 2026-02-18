from flask import Flask, request, redirect
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mypassword",
    database="notesdb"
)

@app.route("/", methods=["GET", "POST"])
def home():
    cursor = db.cursor()

    if request.method == "POST":
        note = request.form["content"]
        cursor.execute("INSERT INTO notes (content) VALUES (%s)", (note,))
        db.commit()
        return redirect("/")

    cursor.execute("SELECT content, created_at FROM notes ORDER BY created_at DESC")
    notes = cursor.fetchall()

    html = """
    <h2>Write a Note</h2>
    <form method="POST">
        <textarea name="content" rows="4" cols="50"></textarea><br><br>
        <button type="submit">Save Note</button>
    </form>
    <hr>
    """

    for note in notes:
        html += f"<p><b>{note[1]}</b><br>{note[0]}</p>"

    return html

app.run(host="0.0.0.0", port=80)
