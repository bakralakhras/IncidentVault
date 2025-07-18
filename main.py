from fastapi import FastAPI
from routes import health, report
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "first run"}

# Include routers
app.include_router(health.router)
app.include_router(report.router)

# Use named instrumentator instance
instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app)

# DEBUG: Print all registered routes
for route in app.routes:
    print(f"🚀 {route.path} -> {route.name}")
