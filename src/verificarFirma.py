from utilidades.archivoUtils import ObtenerRaizProyecto
from utilidades.rsaUtils import CargarClavePublica, VerificarFirmaContenido


# se encarga de verificar la firma del manifiesto utilizando la clave publica para asegurar que el contenido no ha sido alterado desde su firma
def main() -> None:
    RaizProyecto = ObtenerRaizProyecto()
    RutaClavePublica = RaizProyecto / "salidas" / "medisoftPub.pem"
    RutaManifesto = RaizProyecto / "salidas" / "SHA256SUMS.txt"
    RutaFirma = RaizProyecto / "salidas" / "SHA256SUMS.sig"
    try:
        if not RutaManifesto.is_file():
            raise FileNotFoundError(
                f"No se encontro el manifiesto: {RutaManifesto.as_posix()}"
            )
        if not RutaFirma.is_file():
            raise FileNotFoundError(f"No se encontro la firma: {RutaFirma.as_posix()}")

        ClavePublica = CargarClavePublica(RutaClavePublica)
        ContenidoManifesto = RutaManifesto.read_bytes()
        Firma = RutaFirma.read_bytes()
        if VerificarFirmaContenido(ContenidoManifesto, Firma, ClavePublica):
            print("Firma valida")
        else:
            print("Firma invalida")

    except Exception as Error:
        print(f"Error: {Error}")
        raise SystemExit(1) from Error


# llamada de la funcion principal del script
if __name__ == "__main__":
    main()
