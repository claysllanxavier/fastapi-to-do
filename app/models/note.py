from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database.base_class import Base


class Note(Base):
  id = Column(Integer, primary_key=True, index=True)
  Column("text", String),
  Column("completed", Boolean),