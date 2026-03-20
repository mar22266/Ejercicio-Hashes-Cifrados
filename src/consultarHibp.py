from requests import RequestException

from utilidades.hibpUtils import (
    CalcularSha1Mayusculas,
    CalcularSha256Hex,
    ConsultarRangoHibp,
    ObtenerConteoFiltraciones,
)

# contrasenias a probar
ContrasenasPrueba = ["admin", "123456", "hospital", "medisoft2024"]


# consulta cada contrasena y muestra los resultados
def ConsultarContrasena(Contrasena: str) -> None:
    HashSha256 = CalcularSha256Hex(Contrasena)
    HashSha1 = CalcularSha1Mayusculas(Contrasena)
    Prefijo = HashSha1[:5]

    print(f"Contrasena: {Contrasena}")
    print(f"SHA256: {HashSha256}")
    print(f"SHA1: {HashSha1}")
    print(f"PrefijoEnviado: {Prefijo}")
    print(
        "Nota: solo se envia el prefijo SHA1 de 5 caracteres, nunca el hash completo."
    )

    try:
        Coincidencias = ConsultarRangoHibp(Prefijo)
        Conteo = ObtenerConteoFiltraciones(HashSha1, Coincidencias)
        print(f"AparicionesFiltraciones: {Conteo}")
    except RequestException as ErrorRed:
        print(f"AparicionesFiltraciones: No disponible por error de red: {ErrorRed}")
    except Exception as ErrorInesperado:
        print(
            f"AparicionesFiltraciones: No disponible por error inesperado: {ErrorInesperado}"
        )
    print("-" * 80)


# función principal
def main() -> None:
    for Contrasena in ContrasenasPrueba:
        ConsultarContrasena(Contrasena)


if __name__ == "__main__":
    main()
