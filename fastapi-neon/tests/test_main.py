from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from fastapi_neon.settings import TEST_DATABASE_URL
from fastapi_neon.main import app, get_session


def test_create_heroes_main():
    connection_string = str(TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

    engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300)


    SQLModel.metadata.create_all(engine)
    

    with Session(engine) as session:
        


        def get_session_override():
            return session  

        app.dependency_overrides[get_session] = get_session_override  

        client = TestClient(app=app)

        response = client.post(
            "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        )
        app.dependency_overrides.clear()
        data = response.json()

        assert response.status_code == 200
        assert data["name"] == "Deadpond"
        assert data["secret_name"] == "Dive Wilson"
        assert data["age"] is None
        assert data["id"] is not None
