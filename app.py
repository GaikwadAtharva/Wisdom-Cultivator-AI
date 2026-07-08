from flask import Flask, request, render_template, redirect, url_for, Response, session
import uuid

from services.granite import get_granite_response, generate_reflection_title

from services.reflection_manager import (
    create_reflection,
    get_reflection,
    get_all_reflections,
    add_message,
    update_reflection_title,
    delete_reflection,
    get_statistics
)

app = Flask(__name__)
app.secret_key = "wisdom-cultivator-session-key"


def get_user_id():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
    return session["user_id"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat")
def chat():
    user_id = get_user_id()
    reflections = get_all_reflections(user_id)

    if len(reflections) == 0:
        reflection_id = create_reflection(user_id)
        return redirect(url_for("open_reflection", reflection_id=reflection_id))

    latest_reflection = reflections[-1]
    return redirect(url_for("open_reflection", reflection_id=latest_reflection["id"]))


@app.route("/new")
def new_reflection():
    user_id = get_user_id()
    reflection_id = create_reflection(user_id)
    return redirect(url_for("open_reflection", reflection_id=reflection_id))


@app.route("/rename/<int:reflection_id>", methods=["POST"])
def rename_reflection(reflection_id):
    user_id = get_user_id()
    new_title = request.form["new_title"].strip()

    if new_title:
        update_reflection_title(user_id, reflection_id, new_title)

    return redirect(url_for("open_reflection", reflection_id=reflection_id))


@app.route("/delete/<int:reflection_id>")
def delete_reflection_route(reflection_id):
    user_id = get_user_id()
    delete_reflection(user_id, reflection_id)

    reflections = get_all_reflections(user_id)

    if len(reflections) == 0:
        new_id = create_reflection(user_id)
        return redirect(url_for("open_reflection", reflection_id=new_id))

    latest_reflection = reflections[-1]
    return redirect(url_for("open_reflection", reflection_id=latest_reflection["id"]))


@app.route("/export/<int:reflection_id>")
def export_reflection(reflection_id):
    user_id = get_user_id()
    reflection = get_reflection(user_id, reflection_id)

    if reflection is None:
        return redirect(url_for("chat"))

    content = "Wisdom Cultivator AI - Reflection Export\n"
    content += "========================================\n\n"
    content += f"Title: {reflection['title']}\n"
    content += f"Date: {reflection['date']}\n\n"
    content += "Conversation:\n\n"

    for message in reflection["messages"]:
        content += f"You:\n{message['user']}\n\n"
        content += f"Wisdom Cultivator AI:\n{message['ai']}\n\n"
        content += "----------------------------------------\n\n"

    filename = reflection["title"].replace(" ", "_").replace("/", "_") + ".txt"

    return Response(
        content,
        mimetype="text/plain",
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@app.route("/chat/<int:reflection_id>", methods=["GET", "POST"])
def open_reflection(reflection_id):
    user_id = get_user_id()
    reflection = get_reflection(user_id, reflection_id)

    if reflection is None:
        return redirect(url_for("chat"))

    if request.method == "POST":
        user_message = request.form["message"].strip()

        if user_message:
            try:
                conversation_context = ""

                for message in reflection["messages"]:
                    conversation_context += f"User: {message['user']}\n"
                    conversation_context += f"Assistant: {message['ai']}\n\n"

                conversation_context += f"User: {user_message}\nAssistant:"

                ai_response = get_granite_response(conversation_context)

                if reflection["title"] == "New Reflection":
                    title = generate_reflection_title(user_message)
                    update_reflection_title(user_id, reflection_id, title)

            except Exception as e:
                ai_response = f"Error: {e}"

            add_message(user_id, reflection_id, user_message, ai_response)

            return redirect(url_for("open_reflection", reflection_id=reflection_id))

    return render_template(
        "chat.html",
        reflection=get_reflection(user_id, reflection_id),
        reflections=get_all_reflections(user_id),
        stats=get_statistics(user_id)
    )


if __name__ == "__main__":
    app.run(debug=True)