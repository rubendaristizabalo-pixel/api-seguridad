from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from config import JWT_SECRET

#ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

#def validar_token(token: str = Depends(oauth2_scheme)):
#    try:
#        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
#       return payload
#   except JWTError:
#       raise HTTPException(
#           status_code=status.HTTP_401_UNAUTHORIZED,
#           detail="Token inválido o expirado"
#       )

def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

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
