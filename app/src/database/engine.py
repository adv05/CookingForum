from sqlmodel import create_engine
from sqlmodel import SQLModel, Session
from typing import Generator
from pyramid.config import Configurator
from app.src.config import DB_CONFIG


def get_engine():
    url = "postgresql://{user}:{password}@{host}:{port}/{db}".format(
        user=DB_CONFIG['db_user'],
        password=DB_CONFIG['db_password'],
        host=DB_CONFIG['db_host'],
        port=DB_CONFIG['db_port'],
        db=DB_CONFIG['db_name'],
    )

    engine = create_engine(url=url)
    return engine


def get_db():
    try:
        config = Configurator()
        config.scan(
            "app.src.models"
        )  # Scanning folder to import models
        engine = get_engine()
    except IOError:
        print("Failed to connect to database")
        return None, "fail"
    return engine


def create_table() -> bool:
    engine = get_engine()
    try:
        SQLModel.metadata.create_all(engine)
        return True
    except Exception as message:
        print(message, "Unable to create table")
        raise Exception(message)


def insert_data(entry: object) -> bool:
    engine = get_engine()
    try:
        with Session(engine) as session:
            session.add(entry)
            session.commit()
            session.refresh(entry)
        return True
    except Exception as message:
        print("Unable to create object")
        raise Exception(message)


def get_session() -> Generator:
    engine = get_db()
    with Session(engine) as session:
        yield session
