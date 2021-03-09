from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from datetime import datetime

from .. import db
from ..forms import QuestionForm, AnswerForm

from pybo.models import Question

from pybo.views.auth_views import login_required

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
@login_required
def create():
    form = QuestionForm()

    # form.validate_on_submit 함수는 POST 방식으로 전송된 폼 데이터의 정합성을 점검한다. 
    # 즉, 폼을 생성할 때 각 필드에 지정한 DataRequired() 같은 점검 항목에 이상이 없는지 확인한다. 
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date = datetime.now(), user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form = form)


#p.184 질문 수정
@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    # 로그인한 사용자와 질문의 작성자가 다른 경우
    if g.user != question.user:
        flash('수정 권한이 없습니다.')
        return redirect(url_for('questioin.detail', question_id=question_id))
    if request.method == 'POST':
        #<질문수정>을 하고 <저장하기>버튼을 눌렀을 경우
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question) # form 변수에 들어 있는 데이터(화면에 입력되어 있는 데이터)를 question 객체에 적용해 준다. 
            question.modify_date = datetime.now() # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id = question_id))
    else :
        #<질문수정> 버튼을 눌렀을 때 = Get 방식으로 요청되는 경우! 
        #db에서 조회한 데이터를 템플릿에 바로 적용하는 가장 간단한 방법은, 조회한 데이터를 obj 매개변수에 전달하여 폼을 생성하는 것이다. 
        form = QuestionForm(obj=question)
        #QuestionForm의 subject, content 필드에 question 객체의 subject, content의 값이 적용된다!
    return render_template('question/question_form.html', form= form)



@bp.route('/delete/<int:question_id>')
@login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user :
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id = question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

