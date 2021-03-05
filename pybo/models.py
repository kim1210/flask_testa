#__init__.py 파일에서 생성한 SQLAlchemy 객체를 import한다.
from pybo import db

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # (p.162) User 모델 데이터의 id 값을 Question 모델에 포함시킴.
    #db.ForeignKey : 다른 모델과 연결. ondelete='CASCADE': User 모델 데이터가 삭제되면 Question 모델 데이터도 삭제됨.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', nullable=False)
    user = db.relationship('User', backref = db.backref('question_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    
    # 질문 모델과 연결. db.ForeignKey(연결할 기존 모델의 속성, 삭제 연동 설정) - 질문을 삭제하면 해당 질문에 달린 답변도 함께 삭제된다.
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    
    """
    답변 모델에서 질문 모델을 참조. 
    db.relationship(참조할 모델, 역참조 설정 - 질문에서도 답변을 참조하도록..?)

    만약 질문 데이터를 삭제할 때 연관된 답변 데이터가 모두 삭제되기를 바란다면, 
    db.backref 설정에 cascade='all, delete-orphan' 옵션을 추가해야 한다.
    """
    question = db.relationship('Question', backref = db.backref('answer_set', ))

    
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

#회원가입을 위한 모델 p.140
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
