from contextvars import Context
from email import message
from sqlite3 import enable_shared_cache
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Qnas, Answers, Questions, Contexts
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        answer = request.form.get('answer')
        # print(questions)
        # print(answer)

        new_qna = Qnas(sector_id=current_user.sector_id, user_id=current_user.id)
        db.session.add(new_qna)
        db.session.commit()

        new_answer = Answers(qnas_id=new_qna.id, answer=answer)
        db.session.add(new_answer)

        for e in request.form.getlist('question'):
            new_question = Questions(qnas_id=new_qna.id ,question=e)
            db.session.add(new_question)

        for j in request.form.getlist('context'):
            new_context = Contexts(qnas_id=new_qna.id ,context=j)
            db.session.add(new_context)
            
        db.session.commit()
        
    qnas = Qnas.query.all()
    questions = Questions.query.all()
    contexts = Contexts.query.all()
    answers = Answers.query.all()
    return render_template("home.html", user=current_user, qnas=qnas, questions=questions, answers=answers, contexts=contexts)