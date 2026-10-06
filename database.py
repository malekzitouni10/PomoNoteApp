from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey,Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "mysql+pymysql://root:@localhost/projectpy_db"

engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    fullname = Column(String(50))
    username = Column(String(50), unique=True)
    password= Column(String(250))
    tasks = relationship("Task", back_populates="user")
    notes = relationship("Note", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    text = Column(String(255))
    done = Column(Boolean, default=False)
    color = Column(String(20), default="black")
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="tasks")

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, index=True)
    content = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    user = relationship("User", back_populates="notes")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


