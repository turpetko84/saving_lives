from fastapi import APIRouter, Form, HTTPException
import httpx
from ..config import settings
from ..database import get_connection

router = APIRouter(prefix="/api/asana", tags=["asana"])

ASANA_API = "https://app.asana.com/api/1.0"


@router.post("/task")
async def create_asana_task(
    pet_id: int = Form(...),
    name: str = Form(...),
    email: str = Form(""),
    phone: str = Form(""),
    message: str = Form(""),
):
    if not settings.ASANA_TOKEN:
        raise HTTPException(status_code=500, detail="ASANA_TOKEN not configured")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, breed, age, gender, height, weight, color FROM pets WHERE id = ?", (pet_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet_name, breed, age, gender, height, weight, color = row

    task_name = f"Заявка на {pet_name} от {name}"
    notes = (
        f"Питомец: {pet_name}\n"
        f"Порода: {breed}\n"
        f"Возраст: {age}\n"
        f"Пол: {gender}\n"
        f"Рост: {height}\n"
        f"Вес: {weight}\n"
        f"Окрас: {color}\n"
        f"\n"
        f"Сообщение: {message}\n"
        f"Телефон: {phone}\n"
        f"Email: {email}"
    )

    payload = {"data": {"name": task_name, "notes": notes}}
    if settings.ASANA_PROJECT_GID:
        payload["data"]["projects"] = [settings.ASANA_PROJECT_GID]

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{ASANA_API}/tasks",
            json=payload,
            headers={"Authorization": f"Bearer {settings.ASANA_TOKEN}"},
        )

    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"Asana API error: {resp.text}")

    return {"status": "ok", "message": "Задача создана в Asana"}
