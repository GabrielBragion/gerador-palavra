from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from sqlmodel import Field, Session, SQLModel, create_engine, select

from typing import Annotated
from pathlib import Path

class Palavra(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(index=True)
    definicao: str = Field(index=True)
    foto: str  

    @property
    def foto_path(self) -> Path:
        """Retorna o caminho da foto como um objeto Path."""
        return Path(self.foto)


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.mount("/public", StaticFiles(directory="public"), name="public")

@app.get("/")
async def home():
    return FileResponse("public/index.html")