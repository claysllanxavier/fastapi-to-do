from typing import Optional

from pydantic import BaseModel

class NoteBase(BaseModel):
  text: str
  completed: bool

# Properties to receive on note creation
class NoteCreate(NoteBase):
    pass

# Properties to receive on note update
class NoteUpdate(NoteBase):
    pass

# Properties shared by models stored in DB
class NoteInDBBase(NoteBase):
    id: int
    text: str
    completed: bool

    class Config:
        orm_mode = True


# Properties to return to client
class Note(NoteInDBBase):
    pass


# Properties properties stored in DB
class NoteInDB(NoteInDBBase):
    pass