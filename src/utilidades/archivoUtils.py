from pathlib import Path


# utilidades para manejo de archivos y rutas dentro del proyecto
def ObtenerRaizProyecto() -> Path:
    return Path(__file__).resolve().parents[2]


# asegura que el directorio exista creando las carpetas necesarias
def AsegurarDirectorio(RutaDirectorio: str | Path) -> Path:
    Ruta = Path(RutaDirectorio)
    Ruta.mkdir(parents=True, exist_ok=True)
    return Ruta


# obtiene la ruta relativa de un archivo
def ObtenerRutaRelativaProyecto(RutaArchivo: str | Path) -> str:
    Ruta = Path(RutaArchivo).resolve()
    RaizProyecto = ObtenerRaizProyecto()
    try:
        RutaRelativa = Ruta.relative_to(RaizProyecto)
        return RutaRelativa.as_posix()
    except ValueError:
        return Ruta.name


# obtiene la ruta absoluta del archivo a partir de su referencia en el manifiesto
def ObtenerRutaDesdeManifesto(ReferenciaArchivo: str) -> Path:
    RaizProyecto = ObtenerRaizProyecto()
    return (RaizProyecto / ReferenciaArchivo).resolve()


# lee un archivo de texto y devuelve una lista de lineas no vacias eliminando espacios en blanco
def LeerLineasNoVacias(RutaArchivo: str | Path) -> list[str]:
    Ruta = Path(RutaArchivo)
    if not Ruta.is_file():
        raise FileNotFoundError(f"No se encontro el archivo: {Ruta}")

    with Ruta.open("r", encoding="utf-8") as Archivo:
        return [Linea.strip() for Linea in Archivo if Linea.strip()]


# adjunta una lista de lineas a un archivo de texto asegurando que el directorio exista
def AdjuntarLineas(RutaArchivo: str | Path, Lineas: list[str]) -> None:
    Ruta = Path(RutaArchivo)
    AsegurarDirectorio(Ruta.parent)
    with Ruta.open("a", encoding="utf-8", newline="\n") as Archivo:
        for Linea in Lineas:
            Archivo.write(f"{Linea}\n")
