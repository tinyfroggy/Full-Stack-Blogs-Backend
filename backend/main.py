from fastapi import FastAPI

from routers import user_router, blog_router, admin_router

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

version = "1"

app = FastAPI(
  title="Blog API",
  version="1.0.0",
  description="API for blog"
)

app.include_router(user_router.router, tags=["users"], prefix=f"/api/{version}")

app.include_router(blog_router.router, tags=["blogs"], prefix=f"/api/{version}")

app.include_router(admin_router.router, tags=["admins"], prefix=f"/api/{version}")

@app.get("/", tags=["root"])
async def read_root():
  return {"message": "go to the /docs"}

# uvicorn main:app --reload
