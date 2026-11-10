import uvicorn

from server.utils.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "server.app:app",
        host="0.0.0.0",
        port=8088,
        lifespan="on",
        workers=1,
        reload=bool(settings.debug),
    )
