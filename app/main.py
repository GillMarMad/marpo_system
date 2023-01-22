import uvicorn
from fastapi import FastAPI
import extension.AddDataDB as db

from core.config import settings
from api.api import api_router



app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_STR}/openapi.json")
app.include_router(api_router, prefix=settings.API_STR)

@app.on_event("startup")
async def satrtUp():
    # db.addDataFromCSV()
    pass
#

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)