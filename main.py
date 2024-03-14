from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from pymongo import MongoClient



# MongoDB 연결
client = MongoClient()

# 데이터베이스 선택
db = client["memo_db"]
# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'memo_db')

# 컬렉션 선택
collection = db["memos"]
# Collection(Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'memo_db'), 'memos')

app = FastAPI()

class Memo(BaseModel):
    id:str
    content:str
  
@app.post("/memos")
def create_memo(memo:Memo):
    memo = {
        "title": memo.id,
        "content": memo.content
    }
    result = collection.insert_one(memo)
    print(f"Inserted memo with id {result.inserted_id}")
    
@app.get("/memos")
def read_memos():
    memos = collection.find()
    for memo in memos:
        print(memo)

@app.put("/memos/{memo_id}")
# 메모 수정 (Update)
def update_memo(memo_id, title: str, content: str):
    collection.update_one(
        {"_id": memo_id},
        {"$set": {"title": title, "content": content}}
    )
    print(f"Updated memo with id {memo_id}")

@app.delete("/memos/{memo_id}")
# 메모 삭제 (Delete)
def delete_memo(memo_id):
    collection.delete_one({"_id": memo_id})
    print(f"Deleted memo with id {memo_id}")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

# app = FastAPI()


# class Memo(BaseModel):
#     id:str
#     content:str
    
# memos = []


# @app.post("/memos")
# def create_memo(memo:Memo):
#     memos.append(memo)
#     return memo

# @app.get("/memos")
# def read_memo():
#     return memos

# @app.put("/memos/{memo_id}")
# def put_memo(req_memo:Memo):
#     for memo in memos:
#         if memo.id==req_memo.id:
#             memo.content = req_memo.content
#             return '성공했습니다.'
#     return '그런 메모는 없습니다.'

# @app.delete("/memos/{memo_id}")
# def delete_memo(memo_id):
#     for index, memo in enumerate(memos):
#         if memo.id==memo_id:
#             memos.pop(index)
#             return '성공했습니다.'
#     return '그런 메모는 없습니다.'

# app.mount("/", StaticFiles(directory="static", html=True), name="static")