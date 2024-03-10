from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String, DateTime, Enum, Select, Column
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import enum


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class UserStatus(enum.Enum):
    OK = 0
    LOCKED = 5
    DELETED = 10


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    email = Column(String)
    password = Column(String, default='123456')
    reg_time = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(Integer, default=UserStatus.OK)


class TaskStatus(enum.Enum):
    CREATED = 0
    DOING = 5
    DONE = 10

    @classmethod
    def valueof(cls, status: int):
        for v in cls.values():
            if v.value == status:
                return v
        return None


class Task(db.Model):
    id = Column(String, primary_key=True) # pdf_hash
    status = Column(Integer)
    create_time = Column(DateTime, default=datetime.datetime.utcnow)
    start_time = Column(DateTime)
    finish_time = Column(DateTime)


    @classmethod
    def start(cls, pdf_hash: str):
        t = cls.query.filter_by(id=pdf_hash).first()
        if t:
            t.status = TaskStatus.DOING.value
            t.start_time = datetime.datetime.utcnow()
            db.session.commit()

    @classmethod
    def finish(cls, pdf_hash: str):
        t = cls.query.filter_by(id=pdf_hash).first()
        if t:
            t.status = TaskStatus.DONE.value
            t.finish_time = datetime.datetime.utcnow()
            db.session.commit()

    @classmethod
    def get(cls, pdf_hash: str):
        return cls.query.filter_by(id=pdf_hash).first()
    
    @classmethod
    def next(cls):
        t = cls.query.filter_by(status=TaskStatus.DOING.value).first()
        if t:
            return t
        else:
            return cls.query.filter_by(status=TaskStatus.CREATED.value).order_by(cls.create_time).first()
    


class Pdf(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, default=0)
    hash = Column(String, unique=True)
    name = Column(String)
    total_page_num = Column(Integer, default=0)

    @classmethod
    def get_by_hash(cls, hash: str):
        return cls.query.filter_by(hash = hash).first()


class Page(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pdf_id = Column(Integer, nullable=False)
    page_num = Column(Integer, default=0)
    page_content = Column(String, default="")

    def to_dict(self):
        return {
            # 'id': self.id,
            # 'pdf_id': self.pdf_id,
            'page_num': self.page_num,
            'page_content': self.page_content
        }

    @classmethod
    def query_by_pdf_id(cls, pdf_id: int):
        pages = cls.query.filter_by(pdf_id=pdf_id).all()
        pages_dict = [page.to_dict() for page in pages]
        return pages_dict

    @classmethod
    def save(cls, page):
        db.session.add(page)
        db.session.commit()

    @classmethod
    def get_max_page_num(cls, pdf_id: int):
        page = cls.query.filter_by(pdf_id=pdf_id).order_by(cls.page_num.desc()).first()
        if page:
            return page.page_num
        else:
            return -1
