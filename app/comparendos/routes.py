from fastapi import APIRouter, Depends
from app.database import get_connection
from app.rate_limit import rate_limit
from app.security import validar_token, requiere_roles

router = APIRouter()

# -------------------------------
# 1️⃣ GET – LISTADO SIMPLE
# -------------------------------
@router.get("/comparendos/fecha_hecho/{anio}")
def listar_comparendos_anio(
    anio: int,
    usuario=Depends(validar_token)
):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            num_expediente,
            nom_depto,
            nom_mpio,
            hora_hecho,
            nom_comuna_hecho,
            nom_barrio_hecho,
            sitio_hecho,
            dire_hecho,
            lat,
            lon,
            num_comparendo,
            num_articulo,
            comportamiento,
            num_infractor,
            edad_infractor,
            nacionalidad_infractor,
            pob_vulnerable,
            tipo_documento,
            pais_reside,
            dto_reside,
            mun_reside,
            tipo_bien,
            clase_bien,
            cant_incautado,
            unidad_incautado,
            valor_incautado,
            cod_barrio,
            nom_barrio,
            cod_comuna,
            estrato,
            cod_corregimiento,
            nom_corregimiento,
            agrupado,
            rango_edad,
            rango_hora,
            geom,
            fecha_hecho
        FROM alertas_vbg.comparendos
        WHERE EXTRACT(YEAR FROM fecha_hecho) = %s
    """, (anio,))

    rows = cur.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron registros para el año consultado"
        )

    columnas = [desc[0] for desc in cur.description]
    data = [dict(zip(columnas, fila)) for fila in rows]

    cur.close()
    conn.close()

    return {
        "anio": anio,
        "total_registros": len(data),
        "resultados": data
    }

# -------------------------------
# 1️⃣ GET – LISTADO COMPARENDOS POR CEDULA
# -------------------------------
@router.get("/comparendos/num_infractor/{cedula}")
def listar_comparendos_cedula(
    cedula: str,
    usuario=Depends(validar_token)
):
    
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            num_expediente,
            nom_depto,
            nom_mpio,
            hora_hecho,
            nom_comuna_hecho,
            nom_barrio_hecho,
            sitio_hecho,
            dire_hecho,
            lat,
            lon,
            num_comparendo,
            num_articulo,
            comportamiento,
            num_infractor,
            edad_infractor,
            nacionalidad_infractor,
            pob_vulnerable,
            tipo_documento,
            pais_reside,
            dto_reside,
            mun_reside,
            tipo_bien,
            clase_bien,
            cant_incautado,
            unidad_incautado,
            valor_incautado,
            cod_barrio,
            nom_barrio,
            cod_comuna,
            estrato,
            cod_corregimiento,
            nom_corregimiento,
            agrupado,
            rango_edad,
            rango_hora,
            fecha_hecho
        FROM alertas_vbg.comparendos
        WHERE num_infractor = %s
    """, (cedula,))

    rows = cur.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron registros para la cédula consultada"
        )

    columnas = [desc[0] for desc in cur.description]
    data = [dict(zip(columnas, fila)) for fila in rows]

    cur.close()
    conn.close()

    return {
        "Cédula": cedula,
        "total_registros": len(data),
        "resultados": data
    }

# -------------------------------
# 1️⃣ GET – LISTADO COMPARENDOS POR AGRUPADO
# -------------------------------
@router.get("/comparendos/agrupado/{agrupado}")
def listar_comparendos_agrupado(
    agrupado: str,
    usuario=Depends(validar_token)
):
  
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            num_expediente,
            nom_depto,
            nom_mpio,
            hora_hecho,
            nom_comuna_hecho,
            nom_barrio_hecho,
            sitio_hecho,
            dire_hecho,
            lat,
            lon,
            num_comparendo,
            num_articulo,
            comportamiento,
            num_infractor,
            edad_infractor,
            nacionalidad_infractor,
            pob_vulnerable,
            tipo_documento,
            pais_reside,
            dto_reside,
            mun_reside,
            tipo_bien,
            clase_bien,
            cant_incautado,
            unidad_incautado,
            valor_incautado,
            cod_barrio,
            nom_barrio,
            cod_comuna,
            estrato,
            cod_corregimiento,
            nom_corregimiento,
            agrupado,
            rango_edad,
            rango_hora,
            fecha_hecho
        FROM alertas_vbg.comparendos
        WHERE agrupado = %s
    """, (agrupado,))

    rows = cur.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron registros para el agrupado consultado"
        )

    columnas = [desc[0] for desc in cur.description]
    data = [dict(zip(columnas, fila)) for fila in rows]

    cur.close()
    conn.close()

    return {
        "Agrupado": agrupado,
        "total_registros": len(data),
        "resultados": data
    }
    
# -------------------------------
# 1️⃣ GET – LISTADO COMPARENDOS POR AÑO Y AGRUPADO
# -------------------------------
   
@router.get("/comparendos/{anio}")
def listar_comparendos_anio_agrupado(
    anio: int,
    agrupado: str,
    usuario=Depends(validar_token)
):

    conn = get_connection()
    cur = conn.cursor()

    sql = """
        SELECT
            num_expediente,
            nom_depto,
            nom_mpio,
            hora_hecho,
            nom_comuna_hecho,
            nom_barrio_hecho,
            sitio_hecho,
            dire_hecho,
            lat,
            lon,
            num_comparendo,
            num_articulo,
            comportamiento,
            num_infractor,
            edad_infractor,
            nacionalidad_infractor,
            pob_vulnerable,
            tipo_documento,
            pais_reside,
            dto_reside,
            mun_reside,
            tipo_bien,
            clase_bien,
            cant_incautado,
            unidad_incautado,
            valor_incautado,
            cod_barrio,
            nom_barrio,
            cod_comuna,
            estrato,
            cod_corregimiento,
            nom_corregimiento,
            agrupado,
            rango_edad,
            rango_hora,
            geom,
            fecha_hecho
        FROM alertas_vbg.comparendos
        WHERE EXTRACT(YEAR FROM fecha_hecho) = %s 
    """
    
    params = [anio]

    if agrupado:
       sql += " AND agrupado ILIKE %s"
       params.append(f"%{agrupado}%")

    cur.execute(sql, tuple(params))

    rows = cur.fetchall()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail="No se encontraron registros para el año y agrupado consultado"
        )

    columnas = [desc[0] for desc in cur.description]
    data = [dict(zip(columnas, fila)) for fila in rows]

    cur.close()
    conn.close()

    return {
        "anio": anio,
        "agrupado": agrupado,
        "total_registros": len(data),
        "resultados": data
    }
    
    
    
    