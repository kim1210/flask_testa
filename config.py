import os
#현재 수행하고 있는 파일의 위치를 반환한다. 
BASE_DIR =os.path.dirname(__file__)

#데이터베이스 접속 주소
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

#SQLAlchemy의 이벤트를 처리하는 옵션이다. False로 비활성화.
SQLALCHEMY_TRACK_MODIFICATIONS =False

#Flask-WTF를 사용하려면 플라스크 환경 변수 SECRET_KEY가 필요하다. (p.96)
#SECRET_KEY는 CSRF라는 웹 사이트 취약점 공격을 방지하는데 사용한다. 
#CSRF? 사용자의 요청을 위조하는 웹 사이트 공격 기법 
#시크릿키를 기반으로 해서 생성되는 CSRF 토큰은, 폼으로 전송된 데이터가 실제 웹 페이지에서 작성된 데이터인지를 판단해 주는 가늠자 역할을 한다. 
SECRET_KEY = "dev"

