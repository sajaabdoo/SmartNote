from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

NOTES_FILE = "notes.json"

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, "r") as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)

def sort_notes(notes):
    order = {"High": 0, "Medium": 1, "Low": 2}
    return sorted(notes, key=lambda x: order[x["priority"]])

@app.route("/", methods=["GET", "POST"])
def index():
    notes = load_notes()

    # 🔍 البحث
    search_query = request.args.get("search", "")
    if search_query:
        notes = [n for n in notes if search_query.lower() in n["text"].lower()]

    if request.method == "POST":
        action = request.form.get("action")

        # ➕ إضافة
        if action == "add":
            text = request.form.get("note")
            priority = request.form.get("priority")
            notes.append({
                "text": text,
                "priority": priority,
                "word_count": len(text.split()),
                "date": datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            save_notes(notes)
            return redirect(url_for("index"))

        # ❌ حذف
        if action == "delete":
            index = int(request.form.get("index"))
            notes = load_notes()
            notes.pop(index)
            save_notes(notes)
            return redirect(url_for("index"))

        # ✏️ تعديل
        if action == "edit":
            index = int(request.form.get("index"))
            text = request.form.get("note")
            priority = request.form.get("priority")
            notes = load_notes()
            notes[index]["text"] = text
            notes[index]["priority"] = priority
            notes[index]["word_count"] = len(text.split())
            save_notes(notes)
            return redirect(url_for("index"))

    notes = sort_notes(notes)
    total_notes = len(notes)
    total_words = sum(n["word_count"] for n in notes)

    return render_template(
        "index.html",
        notes=notes,
        total_notes=total_notes,
        total_words=total_words,
        search_query=search_query
    )

if __name__ == "__main__":
    app.run(debug=True, port=8000)