from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security import OAuth2PasswordBearer

from server.routes.user import router as userRouter
from server.routes.join_beta import router as joinBetaRouter
from server.routes.search import router as searchRouter
from server.routes.image_like import router as imageLikeRouter
from server.routes.other import router as otherRouter
from server.routes.support_contact import router as supportRouter
from server.routes.generation_history import router as imageGenerationRouter
from server.routes.admin_portal import router as adminConfigRouter
from server.utils.database import Base, SessionLocal, engine

app = FastAPI(
    title="Picsy Docs",
    description="This is the documentation for picsy's API.",
    version="1.0",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url="/admin_docs",
    redoc_url=None,
    basePath="/v1",
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup():
    Base.metadata.create_all(engine)


@app.on_event("shutdown")
async def shutdown():
    db = SessionLocal()
    db.close()


@app.get("/")
def home():
    return {"Picsy's server is running"}


app.include_router(
    searchRouter,
    tags=["Search"],
    prefix="/v1",
)


app.include_router(
    joinBetaRouter,
    tags=["Join Beta"],
    prefix="/v1",
)

app.include_router(
    userRouter,
    tags=["User"],
    prefix="/v1",
)

app.include_router(
    imageLikeRouter,
    tags=["Image Like"],
    prefix="/v1",
)

app.include_router(
    otherRouter,
    tags=["Other"],
    prefix="/v1",
)

app.include_router(
    supportRouter,
    tags=["Support"],
    prefix="/v1",
)

app.include_router(
    imageGenerationRouter,
    tags=["Image Generation"],
    prefix="/v1",
)

app.include_router(
    adminConfigRouter,
    tags=["Admin Config"],
    prefix="/v1",
)
