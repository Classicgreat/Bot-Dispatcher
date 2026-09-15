from sqlalchemy import create_engine,Column,String,Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
Base=declarative_base()
class User(Base):
    __tablename__="users"
    id=Column(String, primary_key=True)
    chat_id=Column(String)
    admin=Column(Integer)
    def __repr__(self):
        return f"<User(id={self.id}, chat_id={self.chat_id}, admin={self.admin})>"
class Database:
    def __init__(self,datbaz)->None:
        self.engine=create_engine(f"sqlite:///{datbaz}.db")
        Base.metadata.create_all(self.engine)
        Session=sessionmaker(bind=self.engine)
        self.session=Session()
    
    def get(self,id):
        return self.session.query(User).filter_by(id=id).first()
    def get_all(self):
        return self.session.query(User).all()
    def register(self,id,chat_id):
        user=User(id=id,chat_id=chat_id,admin=0)
        self.session.add(user)
        self.session.commit()
        return True
        
    def __del__(self):
        self.session.close()