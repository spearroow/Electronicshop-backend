from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence, func

Base = declarative_base()

class ShopItem(Base):
    __tablename__ = "items"
    id = Column(Integer, Sequence("item_id_seq"), primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer)
    note = Column(String)
    category = Column(String)
    purchased = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
