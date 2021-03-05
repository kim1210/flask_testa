from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    #POST 방식 요청에는 계정 등록을, GET 방식 요청에는 계정 등록을 하는 템플릿 렌더링.
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, 
                        password = generate_password_hash(form.password1.data),
                        email = form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else :
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    # p.151
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error= None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        # 데이터베이스에 저장된 비밀번호는 암호화되었으므로 입력된 비밀번호와 바로 비교할 수 없다. 
        # 입력된 비밀번호는 반드시 check_password_hash 함수로 똑같이 암호화하여 비교해야 한다. 
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            #사용자도 존재하고 비밀번호도 올바르다면 플라스크 session에 키와 키값을 저장한다. 
            session.clear()
            #키에는 'user_id'라는 문자열을 저장하고 키값은 데이터베이스에서 조회된 사용자의 id 값을 저장한다.
            session['user_id']=user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

'''
(p.152)
웹 프로그램은 [웹 브라우저 요청 -> 서버 응답] 순서로 실행되며, 
서버 응답이 완료되면 웹 브라우저와 서버 사이의 연결은 끊어진다.

그렇다면 서버는 수많은 웹 브라우저에서 요청한 것 중에서 같은 브라우저에서 요청한 것인지 아닌지를 어떻게 구별할까?

Cookie : 웹 브라우저를 구별하는 값 
웹 브라우저가 요청하면 서버는 쿠키를 생성하여 전송하는 방식으로 응답한다. 
그러면 웹 브라우저는 서버에서 받은 쿠키를 저장한다.

이후 서버에 다시 요청할 때는 이 쿠키를 전송한다. 
그러면 서버는 웹 브라우저가 보낸 쿠키를 보고 이전에 보냈던 쿠키와 비교한다. 
이런 방식으로 같은 웹 브라우저에서 요청한 것인지 아닌지를 구분할 수 있다. 

이때 세션은 바로 쿠키 1개당 생성되는 서버의 메모리 공간이라고 할 수 있다. 

단, 세션은 시간제한이 이어서 일정 시간 접속하지 않으면 자동으로 삭제된다. 
'''

@bp.before_app_request
#before_app_request 애너테이션이 적용된 함수는 라우트 함수보다 먼저 실행된다. 
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        '''g는 플라스크가 제공하는 컨텍스트 변수이다.
        이 변수는 request 변수와 마찬가지로 [요청 -> 응답] 과정에서 유효하다. 
        코드에서 보듯 session 변수에 user_id 값이 있으면 데이터베이스에서 이를 조회하여 g.user에 저장한다. 
        
        이렇게 하면 이후 사용자 로그인 검사를 할 때 session을 조사할 필요가 없다. 
        g.user에 값이 있는지만 알아내면 된다. 
        g.user에는 User 객체가 저장되어 있으므로 여러 가지 사용자 정보(username, email 등)를 추가로 얻어내는 이점이 있다. 
        ''' 

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
#로그아웃 함수에는 세션의 모든 값을 삭제할 수 있도록 session.clear()를 추가
#따라서 session에 저장된 user_id는 삭제될 것이며, 
#앞서 작성한 load_logged_in_user 함수에서 session의 값을 읽을 수 없으므로 g.user는 None이 될 것이다.
