import hashlib
import requests

# url de consulta de rangos de hashes en HIBP y encabezados personalizados para la API
UrlBaseHibp = "https://api.pwnedpasswords.com/range"
EncabezadosHibp = {
    "User-Agent": "MediSoftHashesAcademico/1.0",
}


# funciones para calcular hashes y consultar HIBP
def CalcularSha1Mayusculas(Texto: str) -> str:
    return hashlib.sha1(Texto.encode("utf-8")).hexdigest().upper()


def CalcularSha256Hex(Texto: str) -> str:
    return hashlib.sha256(Texto.encode("utf-8")).hexdigest()


def ConsultarRangoHibp(Prefijo: str, TiempoEspera: int = 10) -> dict[str, int]:
    Url = f"{UrlBaseHibp}/{Prefijo}"
    Respuesta = requests.get(Url, headers=EncabezadosHibp, timeout=TiempoEspera)
    Respuesta.raise_for_status()

    Coincidencias: dict[str, int] = {}
    for Linea in Respuesta.text.splitlines():
        if ":" not in Linea:
            continue
        Sufijo, Conteo = Linea.strip().split(":", maxsplit=1)
        if not Conteo.isdigit():
            continue
        Coincidencias[Sufijo.upper()] = int(Conteo)
    return Coincidencias


# obtiene el conteo de filytrasiones
def ObtenerConteoFiltraciones(
    HashSha1Mayusculas: str, CoincidenciasRango: dict[str, int]
) -> int:
    Sufijo = HashSha1Mayusculas[5:]
    return CoincidenciasRango.get(Sufijo, 0)
