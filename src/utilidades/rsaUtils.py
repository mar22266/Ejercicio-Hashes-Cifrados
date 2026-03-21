from pathlib import Path
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15


# genera el par de claves RSA con el tamaño especificado
def GenerarParClavesRsa(TamanoBits: int = 2048) -> tuple[RSA.RsaKey, RSA.RsaKey]:
    ClavePrivada = RSA.generate(TamanoBits)
    ClavePublica = ClavePrivada.publickey()
    return ClavePrivada, ClavePublica


# guarda una clave RSA en formato PEM
def GuardarClavePem(Clave: RSA.RsaKey, RutaSalida: str | Path) -> None:
    Ruta = Path(RutaSalida)
    Ruta.parent.mkdir(parents=True, exist_ok=True)
    with Ruta.open("wb") as Archivo:
        Archivo.write(Clave.export_key())


# genera la clave privada a partir de un archivo PEM
def CargarClavePrivada(RutaArchivo: str | Path) -> RSA.RsaKey:
    Ruta = Path(RutaArchivo)
    if not Ruta.is_file():
        raise FileNotFoundError(f"No se encontro la clave privada: {Ruta}")

    with Ruta.open("rb") as Archivo:
        return RSA.import_key(Archivo.read())


# genera la clave publica a partir de un archivo PEM
def CargarClavePublica(RutaArchivo: str | Path) -> RSA.RsaKey:
    Ruta = Path(RutaArchivo)
    if not Ruta.is_file():
        raise FileNotFoundError(f"No se encontro la clave publica: {Ruta}")

    with Ruta.open("rb") as Archivo:
        return RSA.import_key(Archivo.read())


# firma el contenido utilizando la clave privada y devuelve la firma en bytes
def FirmarContenido(Contenido: bytes, ClavePrivada: RSA.RsaKey) -> bytes:
    Resumen = SHA256.new(Contenido)
    return pkcs1_15.new(ClavePrivada).sign(Resumen)


# verifica la firma del contenido utilizando la clave publica y devuelve True si es valida o False si no lo es
def VerificarFirmaContenido(
    Contenido: bytes, Firma: bytes, ClavePublica: RSA.RsaKey
) -> bool:
    Resumen = SHA256.new(Contenido)
    try:
        pkcs1_15.new(ClavePublica).verify(Resumen, Firma)
        return True
    except (ValueError, TypeError):
        return False
