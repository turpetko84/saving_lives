import os
import time
from fastapi import APIRouter, Request, Form, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import bcrypt
from ..database import get_connection
from ..config import settings

router = APIRouter(prefix="/admin", tags=["admin"])
templates = Jinja2Templates(directory="app/templates")

IMAGES_DIR = "/app/images"


def check_auth(request: Request) -> bool:
    return request.cookies.get("admin_auth") == "1"


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    if check_auth(request):
        return RedirectResponse(url="/admin/dashboard", status_code=302)
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT password_hash FROM admins WHERE username = ?", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row and bcrypt.checkpw(password.encode(), row[0].encode()):
        response = RedirectResponse(url="/admin/dashboard", status_code=302)
        response.set_cookie("admin_auth", "1", httponly=True, max_age=86400)
        return response

    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверное имя пользователя или пароль"})


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/admin/login", status_code=302)
    response.delete_cookie("admin_auth")
    return response


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, name, breed, age, image_path FROM pets ORDER BY id")
    pets = [{"id": r[0], "name": r[1], "breed": r[2], "age": r[3], "image_path": r[4]} for r in cur.fetchall()]

    cur.execute("""
        SELECT a.id, a.name, a.email, a.phone, a.message, a.status, a.created_at, p.name
        FROM applications a LEFT JOIN pets p ON a.pet_id = p.id
        ORDER BY a.created_at DESC
    """)
    applications = [
        {"id": r[0], "name": r[1], "email": r[2], "phone": r[3],
         "message": r[4], "status": r[5], "created_at": r[6], "pet_name": r[7]}
        for r in cur.fetchall()
    ]

    cur.execute("SELECT COUNT(*) FROM pets")
    pet_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applications")
    app_count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "pets": pets,
        "applications": applications,
        "pet_count": pet_count,
        "app_count": app_count,
    })


@router.post("/applications/{app_id}/status")
def update_application_status(request: Request, app_id: int, status: str = Form(...)):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    if status not in ("new", "reviewed", "approved", "rejected"):
        raise HTTPException(status_code=400, detail="Invalid status")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE applications SET status = ? WHERE id = ?", (status, app_id))
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.post("/pets")
async def create_pet(
    request: Request,
    name: str = Form(...),
    breed: str = Form(""),
    age: str = Form(""),
    gender: str = Form(""),
    height: str = Form(""),
    weight: str = Form(""),
    color: str = Form(""),
    description: str = Form(""),
    photo: UploadFile = File(None),
):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    image_path = ""
    if photo and photo.filename:
        ext = os.path.splitext(photo.filename)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            ext = ".jpg"
        filename = f"pet_{int(time.time())}{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)
        content = await photo.read()
        with open(filepath, "wb") as f:
            f.write(content)
        image_path = f"images/{filename}"

    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pets (name, breed, age, gender, height, weight, color, description, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (name, breed, age, gender, height, weight, color, description, image_path),
    )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.get("/pets/{pet_id}/edit", response_class=HTMLResponse)
def edit_pet_page(request: Request, pet_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, breed, age, gender, height, weight, color, description, image_path FROM pets WHERE id = ?", (pet_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Pet not found")

    pet = {
        "id": row[0], "name": row[1], "breed": row[2], "age": row[3],
        "gender": row[4], "height": row[5], "weight": row[6], "color": row[7],
        "description": row[8], "image_path": row[9],
    }
    return templates.TemplateResponse("edit_pet.html", {"request": request, "pet": pet})


@router.post("/pets/{pet_id}/edit")
async def update_pet(
    request: Request,
    pet_id: int,
    name: str = Form(...),
    breed: str = Form(""),
    age: str = Form(""),
    gender: str = Form(""),
    height: str = Form(""),
    weight: str = Form(""),
    color: str = Form(""),
    description: str = Form(""),
    photo: UploadFile = File(None),
):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    conn = get_connection()
    cur = conn.cursor()

    # Get current image_path
    cur.execute("SELECT image_path FROM pets WHERE id = ?", (pet_id,))
    row = cur.fetchone()
    if not row:
        cur.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Pet not found")

    image_path = row[0]

    # Handle new photo upload
    if photo and photo.filename:
        ext = os.path.splitext(photo.filename)[1].lower()
        if ext not in (".jpg", ".jpeg", ".png", ".gif", ".webp"):
            ext = ".jpg"
        filename = f"pet_{int(time.time())}{ext}"
        filepath = os.path.join(IMAGES_DIR, filename)
        content = await photo.read()
        with open(filepath, "wb") as f:
            f.write(content)
        image_path = f"images/{filename}"

    cur.execute(
        "UPDATE pets SET name=?, breed=?, age=?, gender=?, height=?, weight=?, color=?, description=?, image_path=? WHERE id=?",
        (name, breed, age, gender, height, weight, color, description, image_path, pet_id),
    )
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/admin/dashboard", status_code=302)


@router.post("/pets/{pet_id}/delete")
def delete_pet(request: Request, pet_id: int):
    if not check_auth(request):
        return RedirectResponse(url="/admin/login", status_code=302)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pets WHERE id = ?", (pet_id,))
    conn.commit()
    cur.close()
    conn.close()

    return RedirectResponse(url="/admin/dashboard", status_code=302)
