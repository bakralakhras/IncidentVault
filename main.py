from fastapi import FastAPI
from routes import health, report
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "first run"}

app.include_router(health.router)
app.include_router(report.router)

instrumentator = Instrumentator()
instrumentator.instrument(app)
instrumentator.expose(app)

for route in app.routes:
    print(f"{route.path} -> {route.name}")
