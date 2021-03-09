from flask import Blueprint, url_for, request, render_template,g
from werkzeug.utils import redirect

from datetime import datetime

from .. import db
from ..forms import AnswerForm
from pybo.models import Question, Answer

#p.174
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        content = request.form['content']
        #g.user는 auth_views.py의 @bp.before_app_request로 만든 로그인 사용자 정보이다. (p.172)
        answer =Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
    #답변 저장을 위해 다음 코드를 사용할 수도 있다.
    #answer = Answer(question=question, content=content, create_date=datetime.now())
    #db.session.ad(answer)

        db.session.commit()
        #return redirect(url_for('question.detail', question_id=question_id))
        #(p.233)위의 코드를 앵커 엘리먼트로 이동할 수 있도록 아래와 같이 수정함.
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    return render_template('question/question_detail.html', question=question, form = form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user != answer.user :
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id = answer.question.id))
    if request.method =="POST" :
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer)
            answer.modify_date = datetime.now() #수정일시 저장
            db.session.commit()
            #return redirect(url_for('question.detail', question_id = answer.question.id))를 아래로 수정(p.233)
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id), answer.id))
    else :
        form = AnswerForm(obj=answer)
    return render_template('answer/answer_form.html', answer=answer, form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user :
        flash('삭제권한이 없습니다')
    else :
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))
    
