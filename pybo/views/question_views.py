from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from datetime import datetime

from .. import db
from ..forms import QuestionForm, AnswerForm

from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default=1) #페이지
    question_list = Question.query.order_by(Question.create_date.desc())
    #paginate 함수는 조회한 데이터를 감싸 Pagination 객체로 반환한다. 
    #아래 코드에서 question_list는 paginate 함수를 사용해 Pagination 객체가 되었다. (p.124)
    question_list = question_list.paginate(page, per_page=10)
    return render_template('question/question_list.html', question_list = question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    #get_or_404 함수는 해당 데이터를 찾을 수 없는 경우에 404페이지를 출력해 준다.
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question = question, form = form)

@bp.route('/create/', methods=('GET', 'POST'))
def create():
    form = QuestionForm()

    # form.validate_on_submit 함수는 POST 방식으로 전송된 폼 데이터의 정합성을 점검한다. 
    # 즉, 폼을 생성할 때 각 필드에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인한다. 
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date = datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form = form)