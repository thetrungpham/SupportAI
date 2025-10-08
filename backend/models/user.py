'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.session import Base
from sqlalchemy.orm import Session


# Mô hình User trong cơ sở dữ liệu
class User(Base):
    __tablename__ = "user"  # Tên bảng trong cơ sở dữ liệu

    id = Column(Integer, primary_key=True, index=True)  # ID người dùng
    username = Column(String, unique=True, index=True, nullable=False)  # Tên người dùng
    hashed_password = Column(String, nullable=False)  # Mật khẩu đã mã hóa

    archives = relationship("Archive", back_populates="user", cascade="all, delete-orphan")  # Mối quan hệ với bảng Chat


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
'''