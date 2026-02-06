from fastapi import APIRouter, Depends
from app.database import get_connection
from app.security import validar_token
from app.rate_limit import rate_limit
from app.security import requiere_roles

router = APIRouter()

# -------------------------------
# 1️⃣ GET – LISTADO SIMPLE
# -------------------------------
@router.get("/vbg/num_documento/{cedula}")
def listar_vbg_cedula(
cedula: str,
usuario=Depends(validar_token)):
    
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT tipo_documento, num_documento, edad, marca_temporal, tipo_atencion, prof_atencion1, prof_atencion2, nacionalidad, municipio_procede, municipio_procede_otro, tipo_zona, id_comuna, nom_corregimiento, nom_barrio, estrato_socioeconomico, tipo_sexo, identidad_genero, orientacion_sexual, estado_civil, cant_hijos, cabeza_familia, ocupa_actual, ocupa_actual_otro, entidad_promotora_salud, regimen_salud, nivel_escolaridad, tipo_etnia, grupo_poblacional, tipo_discapacidad, v_fisica, v_verbal, v_psicologica, v_sexual, v_economica, v_patrimonial, v_estructural, v_vicaria, riesgo_feminicidio, remision_entidad, comentarios, entidad, year, month, day, day_year, day_week, week_year, iso_week, iso_year, fecha_atencion FROM alertas_vbg.consolidado_vbg
WHERE num_documento = %s""",(cedula,))

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

