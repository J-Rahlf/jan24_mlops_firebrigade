from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext

app = FastAPI()
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users = {
    "harriet": {
        "username": "harriet",
        "name": "Harriet Kane",
        "hashed_password": pwd_context.hash('munich2024'),
    },
    "phil": {
        "username": "phil",
        "name": "Phil Foden",
        "hashed_password": pwd_context.hash('manchester2024'),
    }
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not (users.get(username)) or not (pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/login")
def current_user(username: str = Depends(get_current_user)):
    return "Hello {}".format(username)

@app.post("/logout")
async def logout():
    return {"message": "Logout successful"}
