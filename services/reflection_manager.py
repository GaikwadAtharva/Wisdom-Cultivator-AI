import json
import os
from datetime import datetime

DATA_FILE = "data/reflections.json"


def load_reflections():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_reflections(reflections):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(reflections, file, indent=4, ensure_ascii=False)


def create_reflection():
    reflections = load_reflections()

    new_id = 1
    if reflections:
        new_id = max(r["id"] for r in reflections) + 1

    reflection = {
        "id": new_id,
        "title": "New Reflection",
        "date": datetime.now().strftime("%d %b %Y • %I:%M %p"),
        "messages": []
    }

    reflections.append(reflection)
    save_reflections(reflections)

    return new_id


def get_reflection(reflection_id):
    reflections = load_reflections()

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            return reflection

    return None


def update_reflection_title(reflection_id, title):
    reflections = load_reflections()

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            reflection["title"] = title
            break

    save_reflections(reflections)


def add_message(reflection_id, user, ai):
    reflections = load_reflections()

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            reflection["messages"].append({
                "user": user,
                "ai": ai
            })
            break

    save_reflections(reflections)


def delete_reflection(reflection_id):
    reflections = load_reflections()

    reflections = [
        reflection for reflection in reflections
        if reflection["id"] != reflection_id
    ]

    save_reflections(reflections)


def get_all_reflections():
    return load_reflections()


def get_statistics():
    reflections = load_reflections()

    total_reflections = len(reflections)

    total_messages = 0

    for reflection in reflections:
        total_messages += len(reflection["messages"])

    latest_date = "No reflections yet"

    if reflections:
        latest_date = reflections[-1]["date"]

    return {
        "total_reflections": total_reflections,
        "total_messages": total_messages,
        "latest_date": latest_date
    }