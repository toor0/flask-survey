from flask import Flask, request, render_template, redirect
from surveys import satisfaction_survey

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []
questions = satisfaction_survey.questions


@app.route('/start')
def start_page():

    title = satisfaction_survey.title
    instruction = satisfaction_survey.instructions

    return render_template("base.html", title=title, instruction=instruction, questions=questions)


@app.route('/question/<int:question_index>')
def handle_question(question_index):
    
    question = questions[question_index].question
    choices = questions[question_index].choices
    question_index = question_index
    return render_template("question.html", question=question, index=question_index, choices=choices)


@app.route('/answer', methods=["POST"])
def post_answer():

    # next_question = request.form['']
    values = request.form
    answer = values[str(len(responses))]
    next_question = len(responses) + 1
    responses.append(answer)

    return redirect(f"/question/{next_question}")
