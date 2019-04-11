from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.secret_key = 'jacqueeee'

debug = DebugToolbarExtension(app)

# responses = []
questions = satisfaction_survey.questions


@app.route('/start')
def start_page():

    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions

    return render_template("base.html", title=title, instruction=instruction, questions=questions)


@app.route('/set-cookie', methods=["POST"])
def set_cookie():
    
    session["responses"] = []
    current_question = 0

    return redirect(f"/question/{current_question}")


@app.route('/question/<int:question_index>')
def handle_question(question_index):
    if len(session["responses"]) == len(questions):
        return redirect('/thanks')

    current_question_index = len(session["responses"])

    if question_index != current_question_index:
        flash("Trying to access invalid question!")
        return redirect(f"/question/{current_question_index}")

    question = questions[current_question_index].question
    choices = questions[current_question_index].choices
    # question_index = question_index
    return render_template("question.html", question=question, index=current_question_index, choices=choices)


@app.route('/answer', methods=["POST"])
def post_answer():

    # next_question = request.form['']
    values = request.form
    responses = session["responses"]
    answer = values[str(len(responses))]
    responses.append(answer)
    session["responses"] = responses
    next_question = len(responses)
    
    return redirect(f"/question/{next_question}")

@app.route('/thanks')
def thanks():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1> Thanks for completing the survey!</h1>
</body>
</html>"""