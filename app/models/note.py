from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Note(Base):
  __tablename__ = "notes"

  id = Column(Integer, primary_key=True, index=True)
  text = Column(String, nullable=False)
  completed = Column(Boolean, nullable=False)