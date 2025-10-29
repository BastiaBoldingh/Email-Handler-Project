from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey, String, Integer, Boolean, Text, DateTime
from datetime import datetime
from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), nullable=False)
    email: Mapped[str] = mapped_column(String(250), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    accounts = relationship("Account", back_populates="user")

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    email: Mapped[str] = mapped_column(String, nullable=False)
    imap_server: Mapped[str] = mapped_column(String, nullable=False)
    imap_port: Mapped[int] = mapped_column(Integer, default=993)
    imap_ssl: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="accounts")
    folders: Mapped["Folder"] = relationship("Folder", back_populates="account")

class Folder(Base):
    __tablename__ = "folders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account_id: Mapped[int] = mapped_column(Integer, ForeignKey("accounts.id"))
    name: Mapped[str] = mapped_column(String, nullable=False)

    account: Mapped["Account"] = relationship("Account", back_populates="folders")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="folder")

class Message(Base):
    __tablename__ = "messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    folder_id: Mapped[int] = mapped_column(Integer, ForeignKey("folders.id"))
    subject: Mapped[str | None] = mapped_column(String, nullable=True)
    sender: Mapped[str | None] = mapped_column(String, nullable=True)
    recipient: Mapped[str | None] = mapped_column(String, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    body_preview: Mapped[str | None] = mapped_column(Text, nullable=True)

    folder: Mapped["Folder"] = relationship("Folder", back_populates="messages")
    attachments: Mapped[list["Attachment"]] = relationship("Attachment", back_populates="message")

class Attachment(Base):
    __tablename__ = "attachments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(Integer, ForeignKey("messages.id"))
    filename: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str | None] = mapped_column(String, nullable=True)
    size: Mapped[int | None] = mapped_column(Integer, nullable=True)

    message: Mapped["Message"] = relationship("Message", back_populates="attachments")