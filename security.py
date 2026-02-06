from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)

ALGORITHM = "HS256"


# ----------------------------
# Validar token
# ----------------------------
def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM]
        )

        if "user_id" not in payload or "rol" not in payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token malformado"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )


# ----------------------------
# Validar roles
# ----------------------------
def requiere_roles(*roles_permitidos):
    def verificador(usuario=Depends(validar_token)):
        rol = usuario.get("rol")

        if rol not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes"
            )

        return usuario

    return verificador
