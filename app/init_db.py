from app.database import engine
from app.db_models import Base


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("Tabelas criadas com sucesso.")
