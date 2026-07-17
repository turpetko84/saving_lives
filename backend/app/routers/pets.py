import random
from fastapi import APIRouter, HTTPException, Query
from ..database import get_connection

router = APIRouter(prefix="/api/pets", tags=["pets"])


def _row_to_dict(row):
    return {
        "id": row[0], "name": row[1], "breed": row[2], "age": row[3],
        "gender": row[4], "height": row[5], "weight": row[6], "color": row[7],
        "description": row[8], "image_path": row[9],
    }


@router.get("")
def list_pets():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, breed, age, gender, height, weight, color, description, image_path FROM pets ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [_row_to_dict(r) for r in rows]


@router.get("/random")
def random_pets(count: int = Query(default=3, ge=1, le=10)):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, breed, age, gender, height, weight, color, description, image_path FROM pets")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    selected = random.sample(rows, min(count, len(rows)))
    return [_row_to_dict(r) for r in selected]


@router.get("/{pet_id}")
def get_pet(pet_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, breed, age, gender, height, weight, color, description, image_path FROM pets WHERE id = ?", (pet_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Pet not found")
    return _row_to_dict(row)
