from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db, seed_pets, seed_admin, get_connection
from .routers import pets, applications, admin, asana, jira


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    seed_pets()
    seed_admin()
    yield


app = FastAPI(title="\u0421\u043e\u0445\u0440\u0430\u043d\u044f\u044f \u0436\u0438\u0437\u043d\u044c API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pets.router)
app.include_router(applications.router)
app.include_router(admin.router)
app.include_router(asana.router)
app.include_router(jira.router)

templates = Jinja2Templates(directory="app/templates")


@app.get("/pet/{pet_id}")
def pet_page(request: Request, pet_id: int):
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
    return templates.TemplateResponse("pet.html", {"request": request, "pet": pet})


@app.get("/api/stats")
def stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM pets")
    pet_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM applications")
    app_count = cur.fetchone()[0]
    cur.close()
    conn.close()
    return {"pet_count": pet_count, "application_count": app_count}
