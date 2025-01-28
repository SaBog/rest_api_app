from fastapi import APIRouter, FastAPI, Depends
from fastapi.responses import RedirectResponse
from app.routers import organizations, buildings, activities
from app.dependencies import get_api_key

app = FastAPI(
    title="Organizations Directory API",
    version="1.0.0",
    description="REST API для работы со справочником организаций, зданий и деятельностей",
)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

# Define the API prefix
api_prefix = "/api"
router = APIRouter(prefix=api_prefix, 
                   dependencies=[Depends(get_api_key)], 
                   responses={403: {"description": "Operation forbidden"}})

# Include routers with the specified prefix
router.include_router(buildings.router)
router.include_router(organizations.router)
router.include_router(activities.router)

app.include_router(router)