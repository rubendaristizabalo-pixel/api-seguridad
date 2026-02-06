from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

from app.database import get_connection
from app.config import settings

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
BCRYPT_MAX_BYTES = 72


# ----------------------------
# Utils de contraseña
# ----------------------------
def normalize_password(password: str) -> str:
    """
    bcrypt solo soporta hasta 72 bytes.
    Normalizamos a UTF-8 y truncamos de forma segura.
    """
    return password.encode("utf-8")[:BCRYPT_MAX_BYTES].decode(
        "utf-8", errors="ignore"
    )


def verify_password(plain: str, hashed: str) -> bool:
    safe_password = normalize_password(plain)
    return pwd_context.verify(safe_password, hashed)


def hash_password(password: str) -> str:
    safe_password = normalize_password(password)
    return pwd_context.hash(safe_password)


# ----------------------------
# JWT
# ----------------------------
def create_access_token(data: dict, expires_delta: int | None = None) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(
        minutes=expires_delta or ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=ALGORITHM
    )


# ----------------------------
# Token (OAuth2 estándar)
# ----------------------------
@router.post("/token", summary="Generar token JWT")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT id, rol, clave_hash
            FROM alertas_vbg.usuarios
            WHERE usuario = %s
            """,
            (form_data.username,)
        )

        row = cur.fetchone()
        cur.close()
        conn.close()

        # Usuario inexistente o sin hash
        if not row or not row[2]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )

        # Validación de contraseña (bcrypt seguro)
        try:
            if not verify_password(form_data.password, row[2]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario o contraseña incorrectos"
                )
        except ValueError:
            # Error típico de bcrypt (>72 bytes)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Contraseña inválida"
            )

        access_token = create_access_token(
            data={
                "user_id": row[0],
                "rol": row[1]
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    except HTTPException:
        raise
    except Exception as e:
        # Log interno (idealmente usar logging)
        print("ERROR LOGIN:", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en autenticación"
        )
