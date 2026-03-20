import hashlib
from pathlib import Path

# diccionario de algoritmos de hash disponibles para textos y archivos
AlgoritmosTexto = {
    "MD5": hashlib.md5,
    "SHA1": hashlib.sha1,
    "SHA256": hashlib.sha256,
    "SHA3_256": hashlib.sha3_256,
}


# funciones para calcular hashes de textos y archivos
def CalcularHashTexto(Texto: str, Algoritmo: str) -> str:
    if Algoritmo not in AlgoritmosTexto:
        raise ValueError(f"Algoritmo no soportado: {Algoritmo}")

    Hash = AlgoritmosTexto[Algoritmo]()
    Hash.update(Texto.encode("utf-8"))
    return Hash.hexdigest()


# calcula el hash de un archivo utilizando el algoritmo especificado y leyendo el archivo en bloques
def CalcularHashArchivo(
    RutaArchivo: str | Path, Algoritmo: str = "SHA256", TamanoBloque: int = 65536
) -> str:
    if Algoritmo not in AlgoritmosTexto:
        raise ValueError(f"Algoritmo no soportado: {Algoritmo}")

    Ruta = Path(RutaArchivo)
    if not Ruta.is_file():
        raise FileNotFoundError(f"No se encontro el archivo: {Ruta}")

    Hash = AlgoritmosTexto[Algoritmo]()
    with Ruta.open("rb") as Archivo:
        while True:
            Bloque = Archivo.read(TamanoBloque)
            if not Bloque:
                break
            Hash.update(Bloque)
    return Hash.hexdigest()


# calcula la cantidad de bits distintos entre dos hashes hexadecimales
def CalcularBitsDistintosHex(HashHexUno: str, HashHexDos: str) -> int:
    ValorUno = int(HashHexUno, 16)
    ValorDos = int(HashHexDos, 16)
    ResultadoXor = ValorUno ^ ValorDos
    return bin(ResultadoXor).count("1")
