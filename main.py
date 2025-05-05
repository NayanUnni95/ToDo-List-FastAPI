from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def root():
    return "Connection successfully established to the server..."


@app.get("/ping")
def pong():
    return "Pong"


@app.post("/api/signup")
async def signup(name, uname, password):
    return {"name": name, "username": uname, "password": password}
