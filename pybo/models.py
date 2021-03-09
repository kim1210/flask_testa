#__init__.py 파일에서 생성한 SQLAlchemy 객체를 import한다.
from pybo import db

#p.209 테이블 객체 question_voter 생성하기
#SQLAlchemy에 다대다 관계를 적용하도록 계정과 질문이 한 쌍을 이루는 테이블 객체 question_voter를 생성하자.

question_voter = db.Table(
    'question_voter', 
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('questioin_id', db.Integer, db.ForeignKey(
        'question.id', ondelete='CASCADE'), primary_key=True)
)

#테이블 객체? 다대다 관계를 정의하려고 db.Table 클래스로 정의되는 객체

class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # (p.162) User 모델 데이터의 id 값을 Question 모델에 포함시킴.
    #db.ForeignKey : 다른 모델과 연결. ondelete='CASCADE': User 모델 데이터가 삭제되면 Question 모델 데이터도 삭제됨.
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref = db.backref('question_set'))
    # p.182 nullable=True!! 
    modify_date = db.Column(db.DateTime(), nullable=True)
    # p.210  Question 모델에 voter 필드 추가하기
    voter = db.relationship('User', secondary=question_voter, backref = db.backref('question_voter_set'))
    #secondary 설정은 'voter가 다대가 관계이며, question_voter 테이블을 참고한다'는 사실을 알려 준다.
    #또 backref를 question_voter_set로 설정했다. 
    # -> 어떤 계정이 a_user라는 객체로 참조되면 a_user.question_voter_set으로 해당 계정이 추천한 질문 리스트를 구할 수 있게 만들어 준다. ??


#p.211 테이블 객체 answer_voter 생성 후 Answer 모델 수정하기
answer_voter=db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey(
        'answer.id', ondelete='CASCADE'), primary_key=True)
)

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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True)
    #p.212
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))

#회원가입을 위한 모델 p.140
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

#댓글에 사용할 모델 p.197
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True) #댓글 고유번호
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete = 'CASCADE'), nullable=False) #댓글 작성자(User 모델과 관계를 가짐)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False) #댓글 내용
    create_date = db.Column(db.DateTime(), nullable=False) #댓글 작성 일시
    modify_date = db.Column(db.DateTime())
    #질문에 댓글을 작성하면 question_id 필드에 값이 저장되고, 답변에 댓글이 작성되면 answer_id 필드에 값이 저장된다.
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id', ondelete='CASCADE'), nullable=True) #댓글의 질문(Questioin 모델과 관계를 가짐)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True) #댓글의 답변(Answer 모델과 관계를 가짐)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))
    #Comment 모델의 데이터에는 question_id 필드 또는 answer_id 필드 중 하나에만 값이 저장되므로 두 필드는 모두 nullable=True여야 한다. 
