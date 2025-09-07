from flask import Flask, render_template, session, request

app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def index():
    if "display" not in session:
        session["display"] = "0"
    if "current_expression" not in session:
        session["current_expression"] = ""
    if "should_reset" not in session:
        session["should_reset"] = False
    if "error" not in session:
        session["error"] = False

    # Обчислюємо поточний результат для відображення
    current_result = ""
    if session["current_expression"] and not session["error"]:
        try:
            # Перевіряємо ділення на нуль
            if "/0" in session["current_expression"] or "/0." in session["current_expression"]:
                current_result = "Помилка"
            else:
                result = eval(session["current_expression"].replace('×', '*'))
                current_result = str(result)
        except:
            current_result = ""

    return render_template("a.html",
                           display=session["display"],
                           current_result=current_result,
                           current_expression=session["current_expression"],
                           error=session["error"])


@app.route("/click", methods=["POST"])
def click():
    button_value = request.form.get("button")
    session["error"] = False

    if button_value == "clear":
        session["display"] = "0"
        session["current_expression"] = ""
        session["should_reset"] = False

    elif button_value == "ac":
        session["display"] = "0"
        session["current_expression"] = ""
        session["should_reset"] = False

    elif button_value == "delete":
        if session["display"] != "0" and len(session["display"]) > 1:
            session["display"] = session["display"][:-1]
            session["current_expression"] = session["current_expression"][:-1]
        else:
            session["display"] = "0"
            session["current_expression"] = ""

    elif button_value == "percent":
        try:
            current_value = float(session["display"])
            result = current_value / 100
            session["display"] = str(result)
            session["current_expression"] = str(result)
        except:
            session["display"] = "Помилка"
            session["current_expression"] = ""
            session["error"] = True

    elif button_value == "calculate":
        try:
            # Перевіряємо ділення на нуль
            if "/0" in session["current_expression"] or "/0." in session["current_expression"]:
                session["display"] = "Помилка"
                session["current_expression"] = ""
                session["error"] = True
            else:
                expression = session["current_expression"].replace('×', '*')
                result = eval(expression)
                session["display"] = str(result)
                session["current_expression"] = str(result)
                session["should_reset"] = True
        except:
            session["display"] = "Помилка"
            session["current_expression"] = ""
            session["error"] = True
            session["should_reset"] = True

    else:
        if session["should_reset"] or session["error"]:
            session["display"] = ""
            session["current_expression"] = ""
            session["should_reset"] = False
            session["error"] = False

        if session["display"] == "0" and button_value not in ["+", "-", "*", "/", ".", "%"]:
            session["display"] = button_value
            session["current_expression"] = button_value
        else:
            session["display"] += button_value
            session["current_expression"] += button_value

    return index()


if __name__ == "__main__":
    app.run(debug=True)