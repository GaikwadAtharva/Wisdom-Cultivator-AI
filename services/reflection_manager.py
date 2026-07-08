import json
import os
from datetime import datetime

DATA_FOLDER = "data"


def get_data_file(user_id):
    os.makedirs(DATA_FOLDER, exist_ok=True)
    return os.path.join(DATA_FOLDER, f"reflections_{user_id}.json")


def load_reflections(user_id):
    data_file = get_data_file(user_id)

    if not os.path.exists(data_file):
        return []

    try:
        with open(data_file, "r", encoding="utf-8") as file:
            return json.load(file)
    except:
        return []


def save_reflections(user_id, reflections):
    data_file = get_data_file(user_id)

    with open(data_file, "w", encoding="utf-8") as file:
        json.dump(reflections, file, indent=4, ensure_ascii=False)


def create_reflection(user_id):
    reflections = load_reflections(user_id)

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
    save_reflections(user_id, reflections)

    return new_id


def get_reflection(user_id, reflection_id):
    reflections = load_reflections(user_id)

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            return reflection

    return None


def update_reflection_title(user_id, reflection_id, title):
    reflections = load_reflections(user_id)

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            reflection["title"] = title
            break

    save_reflections(user_id, reflections)


def add_message(user_id, reflection_id, user, ai):
    reflections = load_reflections(user_id)

    for reflection in reflections:
        if reflection["id"] == reflection_id:
            reflection["messages"].append({
                "user": user,
                "ai": ai
            })
            break

    save_reflections(user_id, reflections)


def delete_reflection(user_id, reflection_id):
    reflections = load_reflections(user_id)

    reflections = [
        reflection for reflection in reflections
        if reflection["id"] != reflection_id
    ]

    save_reflections(user_id, reflections)


def get_all_reflections(user_id):
    return load_reflections(user_id)


def get_statistics(user_id):
    reflections = load_reflections(user_id)

    total_reflections = len(reflections)
    total_messages = sum(len(reflection["messages"]) for reflection in reflections)

    latest_date = "No reflections yet"

    if reflections:
        latest_date = reflections[-1]["date"]

    return {
        "total_reflections": total_reflections,
        "total_messages": total_messages,
        "latest_date": latest_date
    }