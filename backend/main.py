from fastapi import FastAPI
from sqlalchemy import text
from database.session import get_db, init_db
from endpoints import user_api, archive_api, chat_api
from rag.rag_pipeline import answer_query
from fastapi.middleware.cors import CORSMiddleware
from rag.build import build_vector_store

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print(f"📥 Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"  # ép thêm cho chắc
    return response

# Khởi tạo cơ sở dữ liệu
init_db()

app.include_router(chat_api.router, prefix="/api", tags=["chat"])
app.include_router(archive_api.router, prefix="/api", tags=["archives"])


@app.get("/")
def root():
    return {"message": "Backend is running"}

# Test query tới PostgreSQL
if __name__ == "__main__":
    build_vector_store()
