from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-secret"
students = ["Alice", "Bob", "Charlie"]

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user"] = request.form.get("name")
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/profile")
def profile():
    user = session.get("user")
    return render_template("profile.html", user=user)

@app.route("/")
def home():
    return "Hello Flask!"


@app.route("/students")
def students_list():
    return render_template("students.html", students=students)


@app.route("/students/new")
def new_student():
    return render_template("new_student.html")


@app.route("/students/new", methods=["POST"])
def create_student():
    name = request.form.get("name") 
    if name:  # 防呆：避免空白也被加入
        students.append(name)
    return redirect(url_for("students_list"))


messages = [
    "Hello Flask!",
    "I am learning Jinja",
    "This is message #3"
]

@app.route("/messages")
def show_messages():
    return render_template("messages.html", messages=messages)
    

@app.route("/messages", methods=["POST"])
def create_message():
    content = request.form.get("content")
    if content:
        messages.append(content)
    return redirect("/messages")

@app.route("/delete/<int:index>", methods=["POST"])
def delete_message(index):
    messages.pop(index)
    return redirect("/messages")
    
@app.route("/messages/<int:index>/edit")
def edit_message_page(index):
    old_content = messages[index]
    return render_template("edit_message.html", index=index, old_content=old_content)

@app.route("/messages/<int:index>/edit", methods=["POST"])
def update_message(index):
    new_content = request.form.get("content")
    if new_content:
        messages[index] = new_content
    return redirect("/messages")
    