from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from app.api.v1.routes import router as v1_router

app = FastAPI()

# Custom OpenAPI Schema with Bearer Authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Centella Reinvent Backend",
        version="1.0.0",
        description="API documentation for Centella Reinvent Backend",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Include routes
app.include_router(v1_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Welcome to Centella Reinvent Backend"}
