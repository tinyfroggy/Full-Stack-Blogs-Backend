from fastapi import HTTPException

def handle_exception(status_code: int, detail_message: str) -> HTTPException:
    raise HTTPException(status_code=status_code, detail=detail_message)
