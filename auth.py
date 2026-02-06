from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from database import get_connection
from config import JWT_SECRET

router = APIRouter()

@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, rol FROM alertas_vbg.usuarios WHERE usuario=%s AND clave=%s",
        (form_data.username, form_data.password)
    )
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    access_token = jwt.encode(
        {"user_id": row[0], "rol": row[1]},
        JWT_SECRET,
        algorithm="HS256"
    )

    # 👇 ESTO ES LO CLAVE
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

