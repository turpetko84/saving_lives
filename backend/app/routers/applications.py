from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ..database import get_connection

router = APIRouter(prefix="/api/applications", tags=["applications"])


class ApplicationCreate(BaseModel):
    pet_id: int
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    message: str


@router.post("")
def create_application(app: ApplicationCreate):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM pets WHERE id = ?", (app.pet_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Pet not found")

    cur.execute(
        "INSERT INTO applications (pet_id, name, email, phone, message) VALUES (?, ?, ?, ?, ?)",
        (app.pet_id, app.name, app.email, app.phone, app.message),
    )
    conn.commit()

    cur.execute("SELECT MAX(id) FROM applications")
    new_id = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"id": new_id, "status": "new", "message": "Заявка принята"}
