from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from models.archive import Archive
from pydantic import BaseModel

router = APIRouter(prefix="/archives", tags=["archives"])

# ====================
# Pydantic Schemas
# ====================
class ArchiveCreate(BaseModel):
    archive_id: int
    sender: str   
    content: str

class ArchiveResponse(BaseModel):
    archive_id: int 
    id: int
    sender: str
    message: str

    class Config:
        orm_mode = True
# ====================
# Endpoints
# ====================

# Create archive
@router.post("/", response_model=ArchiveResponse)
def create_archive(archive: ArchiveCreate, db: Session = Depends(get_db)):
    new_archive = Archive(sender=archive.sender, content=archive.content)
    db.add(new_archive)
    db.commit()
    db.refresh(new_archive)
    return {"sender": new_archive.sender, "message": new_archive.content}

# Lấy toàn bộ lịch sử chat
@router.get("/", response_model=list[ArchiveResponse])
def get_archives(db: Session = Depends(get_db)):
    archives = db.query(Archive).order_by(Archive.id).all()
    return [{"archive_id": a.archive_id, "id": a.id,"sender": a.sender, "message": a.content} for a in archives]

@router.get("/{archive_id}", response_model=list[ArchiveResponse])
def get_messages(archive_id: int, db: Session = Depends(get_db)):
    messages = db.query(Archive).filter(Archive.archive_id == archive_id).all()
    if not messages:
        raise HTTPException(status_code=404, detail="No messages found for this archive")
    return [
        ArchiveResponse(archive_id=m.archive_id, id=m.id, sender=m.sender, message=m.content)
        for m in messages
    ]
'''
# Get all archives
@router.get("/", response_model=list[dict])
def get_archives(db: Session = Depends(get_db)):
    archives = db.query(Archive).all()
    return [{"id": a.id, "title": a.title, "content": a.content, "user_id": a.user_id} for a in archives]
# Get archive by ID
@router.get("/{archive_id}", response_model=dict)
def get_archive(archive_id: int, db: Session = Depends(get_db)):
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")
    return {"id": archive.id, "title": archive.title, "content": archive.content, "user_id": archive.user_id}

# Update archive
@router.put("/{archive_id}", response_model=dict)
def update_archive(archive_id: int, update_data: ArchiveUpdate, db: Session = Depends(get_db)):
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")

    if update_data.title:
        archive.title = update_data.title
    if update_data.content:
        archive.content = update_data.content

    db.commit()
    db.refresh(archive)
    return {"message": "Archive updated successfully", "id": archive.id}
'''
# Delete archive
@router.delete("/{archive_id}", response_model=list[ArchiveResponse])
def delete_archive(archive_id: int, db: Session = Depends(get_db)):
    archive = db.query(Archive).filter(Archive.id == archive_id).first()
    if not archive:
        raise HTTPException(status_code=404, detail="Archive not found")

    db.delete(archive)
    db.commit()
    return {"message": "Archive deleted successfully"}
