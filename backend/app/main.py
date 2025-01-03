from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.settings import settings
from api.routers import api_router


app = FastAPI(
    debug=settings.DEBUG_MODE,
    version="1.0.0",
    title="fastapi-onion-template",
    redirect_slashes=False,
    default_response_class=ORJSONResponse,
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # TODO: DONT WORK !!!!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT_BACKEND, reload=True, log_config=settings.LOGGER_CONFIG)
