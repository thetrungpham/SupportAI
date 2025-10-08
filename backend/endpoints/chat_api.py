from pydantic import BaseModel
from sqlalchemy.orm import Session
from database.session import get_db
from models.archive import Archive
from fastapi import APIRouter, Depends, HTTPException
from rag.rag_pipeline import answer_query
from pydantic import BaseModel
from endpoints.archive_api import ArchiveCreate, ArchiveResponse
from typing import Optional

router = APIRouter(prefix="/chat", tags=["chat"])

class QueryRequest(BaseModel):
    archive_id: Optional[int] = None 
    query: str

class QueryResponse(BaseModel):
    archive_id: int
    answer: str

@router.post("/chat", response_model=QueryResponse)
def chat_endpoint(request: QueryRequest, db: Session = Depends(get_db)):
    if request.archive_id is None:
        last_archive = db.query(Archive).order_by(Archive.archive_id.desc()).first()
        new_archive_id = last_archive.archive_id + 1 if last_archive else 1
    else:
        new_archive_id = request.archive_id

    user_msg = Archive(archive_id=new_archive_id, sender="user", content=request.query)
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    response = answer_query(request.query)

    bot_msg = Archive(archive_id=new_archive_id, sender="bot", content=response)
    db.add(bot_msg)
    db.commit()
    db.refresh(bot_msg)
    return QueryResponse(archive_id=new_archive_id, answer=response)


