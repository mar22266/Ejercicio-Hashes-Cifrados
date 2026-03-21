from utilidades.archivoUtils import AsegurarDirectorio, ObtenerRaizProyecto
from utilidades.rsaUtils import GenerarParClavesRsa, GuardarClavePem


# funcion principal donde llama las utilidades para generar el par de claves RSA
def main() -> None:
    try:
        DirectorioSalida = AsegurarDirectorio(ObtenerRaizProyecto() / "salidas")
        ClavePrivada, ClavePublica = GenerarParClavesRsa(2048)
        RutaPrivada = DirectorioSalida / "medisoftPriv.pem"
        RutaPublica = DirectorioSalida / "medisoftPub.pem"
        GuardarClavePem(ClavePrivada, RutaPrivada)
        GuardarClavePem(ClavePublica, RutaPublica)
        print(f"Clave privada generada en: {RutaPrivada.as_posix()}")
        print(f"Clave publica generada en: {RutaPublica.as_posix()}")

    except Exception as Error:
        print(f"Error: {Error}")
        raise SystemExit(1) from Error


if __name__ == "__main__":
    main()
