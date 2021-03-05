from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from datetime import datetime

from .. import db
from ..forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)

    if form.validate_on_submit():
        content = request.form['content']
        answer =Answer(content=content, create_date=datetime.now())
        question.answer_set.append(answer)
    #답변 저장을 위해 다음 코드를 사용할 수도 있다.
    #answer = Answer(question=question, content=content, create_date=datetime.now())
    #db.session.ad(answer)

        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form = form)