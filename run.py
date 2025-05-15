import uvicorn
from decouple import config

API_PORT: int = int(config("API_PORT", default=8000))
API_HOST: str = config("API_HOST", default="127.0.0.1")

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=API_PORT, host=API_HOST, reload=True)
