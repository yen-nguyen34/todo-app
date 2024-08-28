from fastapi import APIRouter, status

router = APIRouter(tags=["Health check"])

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {"status": "ok"}