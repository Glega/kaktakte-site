from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Для простоты разрешаем все, в продакшене лучше указать конкретный домен
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "FastAPI работает!"}

@app.get("/api/data")
def get_data():
    return {"status": "success", "items": ["яблоко", "банан", "апельсин"]}
