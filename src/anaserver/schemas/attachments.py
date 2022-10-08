from pydantic import BaseModel


class AttachmentBase(BaseModel):
    type: int
    url: str


class Attachment(AttachmentBase):
    id: int
    news_id: int

    class Config:
        orm_mode = True
