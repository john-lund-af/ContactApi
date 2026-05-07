from fastapi import FastAPI
from datetime import datetime, timezone, timedelta
from scalar_fastapi import get_scalar_api_reference
from app.routes import contacts

app = FastAPI(
    title="Contact API",
    description="REST API for a contact application",
    version="1.0.0"
)

app.include_router(contacts.router, prefix="/contacts", tags=["contacts"])

start_time: datetime = datetime.now(timezone.utc)

@app.get("/")
def root():
   current_time: datetime = datetime.now(timezone.utc)
   uptime: timedelta = current_time - start_time

   return {
       "status": "ok",
       "app_name": "ContactApi",
       "start_time": start_time,
       "current_time": current_time,
       "uptime_seconds": int(uptime.total_seconds()),
       "uptime": str(uptime)
   }

@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
   return get_scalar_api_reference(
       openapi_url=app.openapi_url,
       title="Scalar API"
   )
