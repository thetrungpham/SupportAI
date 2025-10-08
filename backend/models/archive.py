from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from database.session import Base

class Archive(Base):
    __tablename__ = "archives"  # Tên bảng trong cơ sở dữ liệu
    
    id = Column(Integer, primary_key=True, index=True)
    archive_id = Column(Integer, index=True)  # ID của achirve
    sender = Column(String, nullable=False)  # Tiêu đề của achirve
    content = Column(Text, nullable=False)  # Nội dung của achirve

    #user = relationship("User", back_populates="archives")  

