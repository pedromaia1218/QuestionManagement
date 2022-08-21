from contextvars import Context
from email import message
from sqlite3 import enable_shared_cache
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from flask_login import login_required, current_user
from .models import Qnas, Answers, Questions, Contexts
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        answer = request.form.get('answer')
        # print(questions)
        # print(answer)

        new_qna = Qnas(sector_id=current_user.sector_id,
                       user_id=current_user.id)
        db.session.add(new_qna)
        db.session.commit()

        new_answer = Answers(qnas_id=new_qna.id, answer=answer)
        db.session.add(new_answer)

        for e in request.form.getlist('question'):
            new_question = Questions(qnas_id=new_qna.id, question=e)
            db.session.add(new_question)

        for j in request.form.getlist('context'):
            new_context = Contexts(qnas_id=new_qna.id, context=j)
            db.session.add(new_context)

        db.session.commit()

    qnas = Qnas.query.all()
    questions = Questions.query.all()
    contexts = Contexts.query.all()
    answers = Answers.query.all()
    return render_template("home.html", user=current_user, qnas=qnas, questions=questions, answers=answers, contexts=contexts)


@views.route('/export')
@login_required
def export():
    
    new = request.args.get('new')
    print(new)

    if new is None:
        qnas = Qnas.query.filter_by(check=1)
    else:
        qnas = Qnas.query.filter_by(sent=0, check=1)

    dictionary = {
        "qnas": [],
        "contentElements": []
    }

    for e in qnas:
        e.sent = 1
        db.session.commit()
        questions = Questions.query.filter_by(qnas_id=e.id)
        contexts = Contexts.query.filter_by(qnas_id=e.id)
        answers = Answers.query.filter_by(qnas_id=e.id)
        q = list(map(lambda x: (x.question), questions))
        a = list(map(lambda x: (x.answer), answers))
        c = list(map(lambda x: (x.context), contexts))
        qnas_dict = {
            "id": str(e.id),
            "data": {
                "answers": {
                    "pt": a
                },
                "questions": {
                    "pt": q
                },
                "redirectFlow": "",
                "redirectNode": "",
                "action": "text",
                "enabled": e.enabled,
                "contexts": c
            }
        }
        dictionary["qnas"].append(qnas_dict)

    qnas_json = json.dumps(dictionary, ensure_ascii=False)

    with open("qnas_all.json", "w", encoding='utf-8') as outfile:
        outfile.write(qnas_json)

    path = "../qnas_all.json"
    return send_file(path, as_attachment=True)