from fastapi import Depends, HTTPException, status
from time import time
from app.security import validar_token

# Almacenamiento en memoria (on-premise)
_REQUESTS = {}

# Límites por rol
LIMITES = {
    "ADMIN": 300,   # requests / minuto
    "LECTOR": 60
}

def rate_limit(usuario=Depends(validar_token)):
    user_id = usuario.get("sub") or usuario.get("user_id", "anon")
    rol = usuario.get("rol", "LECTOR")

    limite = LIMITES.get(rol, 30)

    minuto_actual = int(time() // 60)
    clave = f"{user_id}:{minuto_actual}"

    _REQUESTS.setdefault(clave, 0)
    _REQUESTS[clave] += 1

    if _REQUESTS[clave] > limite:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Límite de peticiones excedido ({limite}/min)"
        )

    return True

