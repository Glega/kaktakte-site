import os
import secrets

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


ALLOWED_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "ALLOWED_ORIGINS",
        "https://kaktakte.ru,https://www.kaktakte.ru",
    ).split(",")
    if origin.strip()
]

COOKIE_DOMAIN = os.getenv("COOKIE_DOMAIN", "api.kaktakte.ru") or None
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "true").lower() == "true"
OWNER_PASSWORD = os.getenv("OWNER_PASSWORD", "secret")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Пока фейковые данные.
# Потом заменим на PostgreSQL.
FAKE_USERS = {
    "you": OWNER_PASSWORD,
}

# token -> username
SESSIONS: dict[str, str] = {}


class LoginIn(BaseModel):
    username: str
    password: str


def cookie_kwargs() -> dict:
    return {
        "path": "/",
        "domain": COOKIE_DOMAIN,
        "secure": COOKIE_SECURE,
        "httponly": True,
        "samesite": "lax",
    }


@app.get("/api/health")
def health():
    return {"ok": True}


@app.post("/api/auth/login")
def login(data: LoginIn, response: Response):
    if data.username not in FAKE_USERS:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if data.password != FAKE_USERS[data.username]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = secrets.token_urlsafe(32)
    SESSIONS[token] = data.username

    response.set_cookie(
        key="sid",
        value=token,
        max_age=60 * 60 * 24 * 14,  # 14 дней
        **cookie_kwargs(),
    )

    return {
        "ok": True,
        "user": {
            "username": data.username,
            "role": "owner",
        },
    }


@app.post("/api/auth/logout")
def logout(request: Request, response: Response):
    token = request.cookies.get("sid")

    if token:
        SESSIONS.pop(token, None)

    response.delete_cookie(
        key="sid",
        **cookie_kwargs(),
    )

    return {"ok": True}


def get_current_username(request: Request) -> str:
    token = request.cookies.get("sid")

    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    username = SESSIONS.get(token)

    if not username:
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    return username


@app.get("/api/auth/me")
def me(request: Request):
    username = get_current_username(request)

    return {
        "username": username,
        "role": "owner",
    }
