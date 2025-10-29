from fastapi import FastAPI, Depends
from app.api import routes_users, routes_messages, routes_folders
from sqlalchemy.orm import Session
from app.core.database import get_db, Base, engine
from app.models.db_models import User, Account, Folder, Message, Attachment
from datetime import datetime


app = FastAPI()

# Routing to the other files
app.include_router(routes_users.router, prefix="/users", tags=["Users"])
app.include_router(routes_messages.router, prefix="/messages", tags=["Messages"])
app.include_router(routes_folders.router, prefix="/folders", tags=["Folders"])

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    """
    health check route, inserts a test user, account, folder, message, and attatchement
    :param db:
    :return:
    """
    user_count = db.query(User).count()
    if user_count == 0:
        new_user = User(
            username = "Bastian",
            email = "Email",
            hashed_password = "Hashed Pass"
        )
        db.add(new_user)
        db.commit()
        return "Success"

    return "Hello World"

