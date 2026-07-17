from fastapi import APIRouter, Form, HTTPException
import httpx
from ..config import settings
from ..database import get_connection

router = APIRouter(prefix="/api/jira", tags=["jira"])


def text_to_adf(text):
    paragraphs = []
    for line in text.split("\n"):
        paragraphs.append({
            "type": "paragraph",
            "content": [{"type": "text", "text": line}]
        })
    return {
        "version": 1,
        "type": "doc",
        "content": paragraphs,
    }


@router.post("/task")
async def create_jira_task(
    pet_id: int = Form(...),
    name: str = Form(...),
    email: str = Form(""),
    phone: str = Form(""),
    message: str = Form(""),
):
    if not settings.JIRA_URL or not settings.JIRA_USER_EMAIL or not settings.JIRA_API_TOKEN:
        raise HTTPException(status_code=500, detail="Jira credentials not configured")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, breed, age, gender, height, weight, color FROM pets WHERE id = ?", (pet_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet_name, breed, age, gender, height, weight, color = row

    summary = f"Заявка на {pet_name} от {name}"
    description = (
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

    payload = {
        "fields": {
            "project": {"key": settings.JIRA_PROJECT_KEY},
            "summary": summary,
            "description": text_to_adf(description),
            "issuetype": {"name": "Задание"},
        }
    }

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.JIRA_URL}/rest/api/3/issue",
            json=payload,
            auth=(settings.JIRA_USER_EMAIL, settings.JIRA_API_TOKEN),
            headers={"Content-Type": "application/json"},
        )

    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail=f"Jira API error: {resp.text}")

    return {"status": "ok", "message": "Задача создана в Jira"}
