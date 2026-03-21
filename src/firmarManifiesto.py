from utilidades.archivoUtils import AsegurarDirectorio, ObtenerRaizProyecto
from utilidades.rsaUtils import CargarClavePrivada, FirmarContenido


# lee el manifiesto firma su contenido con la clave privada y guarda la firma en un archivo
def main() -> None:
    RaizProyecto = ObtenerRaizProyecto()
    RutaManifesto = RaizProyecto / "salidas" / "SHA256SUMS.txt"
    RutaClavePrivada = RaizProyecto / "salidas" / "medisoftPriv.pem"
    RutaFirma = RaizProyecto / "salidas" / "SHA256SUMS.sig"

    try:
        if not RutaManifesto.is_file():
            raise FileNotFoundError(
                f"No se encontro el manifiesto: {RutaManifesto.as_posix()}"
            )

        ClavePrivada = CargarClavePrivada(RutaClavePrivada)
        ContenidoManifesto = RutaManifesto.read_bytes()
        Firma = FirmarContenido(ContenidoManifesto, ClavePrivada)
        AsegurarDirectorio(RutaFirma.parent)
        RutaFirma.write_bytes(Firma)
        print(f"Firma generada en: {RutaFirma.as_posix()}")

    except Exception as Error:
        print(f"Error: {Error}")
        raise SystemExit(1) from Error


# llamada de la funcion principal del script
if __name__ == "__main__":
    main()
