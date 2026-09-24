from sqlmodel import SQLModel, create_engine


engine = create_engine(
    "sqlite:///lost_found.db",
    echo=True
)


def create_tables():
    SQLModel.metadata.create_all(engine)