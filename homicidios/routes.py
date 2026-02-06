from fastapi import APIRouter, Depends
from app.database import get_connection
from app.security import validar_token
from app.rate_limit import rate_limit
from app.security import requiere_roles

router = APIRouter()

# -------------------------------
# 1️⃣ GET – LISTADO SIMPLE
# -------------------------------
@router.get("/homicidios")
def listar_homicidios_anio(
anio: int,
usuario=Depends(validar_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""SELECT spoa, fechao, semana, manera_muerte, nacionalidad, tipo_identificacion, cedula, ocupacion, sexo, genero, orientacion, edad, ancestro, estado_civil, escolaridad, barrio, sector, tipo_de_arma, fechah, horah, diasem, nom_lugar_delictivo, lugar_hechos, tipo_violencia, categoria_movil, subcategoria_movil, tipo_agresor, fec_especial, feminicidios, procedimientofuerzapublica, poblacion_lgbtq, licor, drogas, bandas, lgtbi, pandillas, habitantescalle, barras, multiples,idcombar, com, com_hecho, barrioplaneacion, estratoplaneacion, x, y, finsemanaconsecutivo, jornada, jornadarh8, est28xrangohora, fh8,agresor_en_moto, anotaciones, antecedentes, comparendos, movil FROM alertas_vbg.homicidios WHERE fechao = %s AND procedimientofuerzapublica = 'N'""",(anio,))
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

# ==================================================
# 5️⃣ ENDPOINT ESPACIAL (GEOJSON) 👈 AQUÍ SE INTEGRA
# ==================================================
@router.get("/homicidios/geojson")
def homicidios_geojson(usuario=Depends(validar_token)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT json_build_object(
            'type', 'FeatureCollection',
            'features', COALESCE(json_agg(
                json_build_object(
                    'type', 'Feature',
                    'geometry', ST_AsGeoJSON(geom)::json,
                    'properties', json_build_object(
                        'id', id,
                        'nombre', nombre
                    )
                )
            ), '[]'::json)
        )
        FROM alertas_vbg.homicidios;
    """)

    geojson = cur.fetchone()[0]

    cur.close()
    conn.close()
    return geojson
