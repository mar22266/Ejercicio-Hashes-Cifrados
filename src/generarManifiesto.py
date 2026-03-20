import argparse
from pathlib import Path
from utilidades.archivoUtils import (
    AdjuntarLineas,
    ObtenerRaizProyecto,
    ObtenerRutaRelativaProyecto,
)
from utilidades.hashUtils import CalcularHashArchivo


# crear el parser de argumentos para recibir las rutas de los archivos a incluir en el manifiesto
def CrearParser() -> argparse.ArgumentParser:
    Parser = argparse.ArgumentParser(
        description="Genera o actualiza el manifiesto SHA256 de MediSoft."
    )
    Parser.add_argument(
        "RutasArchivos",
        nargs="+",
        help="Lista de archivos para incluir en el manifiesto.",
    )
    return Parser


# valida que las rutas de los archivos existan
def ValidarArchivos(RutasArchivos: list[str]) -> list[Path]:
    if len(RutasArchivos) < 5:
        raise ValueError("Se requieren al menos 5 archivos para generar el manifiesto.")
    ArchivosValidados: list[Path] = []
    for RutaTexto in RutasArchivos:
        Ruta = Path(RutaTexto).resolve()
        if not Ruta.is_file():
            raise FileNotFoundError(f"No se encontro el archivo indicado: {RutaTexto}")
        ArchivosValidados.append(Ruta)
    return ArchivosValidados


# construye las lineas del manifiesto con el hash de cada archivo y su referencia relativa al proyecto
def ConstruirLineasManifesto(Archivos: list[Path]) -> list[str]:
    Lineas: list[str] = []
    for Archivo in Archivos:
        HashArchivo = CalcularHashArchivo(Archivo, "SHA256")
        Referencia = ObtenerRutaRelativaProyecto(Archivo)
        Lineas.append(f"{HashArchivo} {Referencia}")
    return Lineas


# funcion principal donde se parsean los argumentos, se validan los archivos, se construyen las lineas del manifiesto
def main() -> None:
    Parser = CrearParser()
    Argumentos = Parser.parse_args()
    try:
        Archivos = ValidarArchivos(Argumentos.RutasArchivos)
        Lineas = ConstruirLineasManifesto(Archivos)
        RutaManifesto = ObtenerRaizProyecto() / "salidas" / "SHA256SUMS.txt"
        AdjuntarLineas(RutaManifesto, Lineas)
        print(f"Manifesto actualizado: {RutaManifesto.as_posix()}")
        print(f"ArchivosProcesados: {len(Archivos)}")
    except Exception as Error:
        print(f"Error: {Error}")
        raise SystemExit(1) from Error


# funcion de entrada del script
if __name__ == "__main__":
    main()
