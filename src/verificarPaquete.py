from utilidades.archivoUtils import (
    LeerLineasNoVacias,
    ObtenerRaizProyecto,
    ObtenerRutaDesdeManifesto,
)
from utilidades.hashUtils import CalcularHashArchivo


# lee el manifiesto obtiene el hash esperado  calcula el hash actual del archivo y compara ambos para determinar si el archivo esta correcto o alterado
def LeerManifesto() -> list[tuple[str, str]]:
    RutaManifesto = ObtenerRaizProyecto() / "salidas" / "SHA256SUMS.txt"
    if not RutaManifesto.is_file():
        raise FileNotFoundError(
            f"No se encontro el manifiesto: {RutaManifesto.as_posix()}"
        )

    Entradas: list[tuple[str, str]] = []
    for Linea in LeerLineasNoVacias(RutaManifesto):
        Partes = Linea.split(maxsplit=1)
        if len(Partes) != 2:
            continue
        HashEsperado, ReferenciaArchivo = Partes
        Entradas.append((HashEsperado, ReferenciaArchivo))
    return Entradas


# verifica cada entrada del manifiesto calculando el hash actual del archivo
def VerificarEntrada(
    HashEsperado: str, ReferenciaArchivo: str
) -> tuple[str, str, str, str]:
    RutaArchivo = ObtenerRutaDesdeManifesto(ReferenciaArchivo)
    if not RutaArchivo.is_file():
        return ReferenciaArchivo, HashEsperado, "No disponible", "Alterado"

    HashActual = CalcularHashArchivo(RutaArchivo, "SHA256")
    Estado = "Correcto" if HashActual == HashEsperado else "Alterado"
    return ReferenciaArchivo, HashEsperado, HashActual, Estado


# funcion principal que lee el manifiesto y verifica cada entrada mostrando un resumen al final
def main() -> None:
    try:
        Entradas = LeerManifesto()
    except Exception as Error:
        print(f"Error: {Error}")
        raise SystemExit(1) from Error

    TotalArchivos = 0
    Correctos = 0
    Alterados = 0

    for HashEsperado, ReferenciaArchivo in Entradas:
        Archivo, ValorEsperado, ValorActual, Estado = VerificarEntrada(
            HashEsperado, ReferenciaArchivo
        )
        TotalArchivos += 1
        if Estado == "Correcto":
            Correctos += 1
        else:
            Alterados += 1
        print(f"Archivo: {Archivo}")
        print(f"HashEsperado: {ValorEsperado}")
        print(f"HashActual: {ValorActual}")
        print(f"Estado: {Estado}")
        print("-" * 80)
    print(f"TotalArchivos: {TotalArchivos}")
    print(f"Correctos: {Correctos}")
    print(f"Alterados: {Alterados}")


# llamada de la funcion principal del script
if __name__ == "__main__":
    main()
