from flask import Blueprint, url_for

from werkzeug.utils import redirect

#블루프린트 객체 생성 =Blueprint(이름, 모듈명, url프리픽스)
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    # url_for 함수는 라우트가 설정된 함수명으로 URL을 역으로 찾아준다. 
    # question._list는 question, _list 순서로 해석되어 함수명을 찾아준다. 
    # question은 등록된 블루프린트 이름, _list는 블루프린트에 등록된 함수명
    return redirect(url_for('question._list'))