from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/healthcheck", tags=["Health"])
async def healthcheck():
    return JSONResponse(status_code=202, content={"status": "ok"})
