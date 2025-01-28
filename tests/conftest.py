import pytest
import pytest_asyncio
from typing import AsyncGenerator
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings
from app.db.models import Base
from app.db.database import get_db

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create an async engine for the in-memory SQLite database
engine = create_async_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")  # Create a new session for each test function
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield a session to the database and ensure a clean state for each test."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all) 
        await conn.run_sync(Base.metadata.create_all) 

    async with TestingSessionLocal() as session:
        yield session  

@pytest_asyncio.fixture(scope="function")
async def test_client(get_test_session: AsyncSession) -> AsyncGenerator[TestClient, None]:
    """
    Return a FastAPI TestClient that uses the test session.
    """
    async def override_get_db():
        yield get_test_session

    # Override the dependency
    app.dependency_overrides[get_db] = override_get_db 
    
    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def api_key_client(test_client):
    """
    Return a TestClient with the API key set in the headers.
    """
    # Set the API key in the headers
    test_client.headers = {
        "X-API-Key": settings.API_KEY
    }
    return test_client
