from utilidades.hashUtils import CalcularBitsDistintosHex, CalcularHashTexto


# construye una tabla con los hashes de los textos
def ConstruirFilas() -> list[dict[str, str | int]]:
    Textos = ["MediSoft-v2.1.0", "medisoft-v2.1.0"]
    Algoritmos = [
        ("MD5", 128),
        ("SHA1", 160),
        ("SHA256", 256),
        ("SHA3_256", 256),
    ]

    Filas: list[dict[str, str | int]] = []
    for Algoritmo, LongitudBits in Algoritmos:
        for Texto in Textos:
            Hash = CalcularHashTexto(Texto, Algoritmo)
            Filas.append(
                {
                    "Texto": Texto,
                    "Algoritmo": Algoritmo,
                    "LongitudBits": LongitudBits,
                    "LongitudHex": len(Hash),
                    "Hash": Hash,
                }
            )
    return Filas


# imprime la tabla con los hashes de los textos
def ImprimirTabla(Filas: list[dict[str, str | int]]) -> None:
    Encabezados = ["Texto", "Algoritmo", "LongitudBits", "LongitudHex", "Hash"]
    Anchuras = {Encabezado: len(Encabezado) for Encabezado in Encabezados}

    for Fila in Filas:
        for Encabezado in Encabezados:
            Anchuras[Encabezado] = max(Anchuras[Encabezado], len(str(Fila[Encabezado])))

    Separador = " | ".join("-" * Anchuras[Encabezado] for Encabezado in Encabezados)
    EncabezadoTabla = " | ".join(
        f"{Encabezado:<{Anchuras[Encabezado]}}" for Encabezado in Encabezados
    )

    print(EncabezadoTabla)
    print(Separador)
    for Fila in Filas:
        print(
            " | ".join(
                [
                    f"{str(Fila['Texto']):<{Anchuras['Texto']}}",
                    f"{str(Fila['Algoritmo']):<{Anchuras['Algoritmo']}}",
                    f"{str(Fila['LongitudBits']):<{Anchuras['LongitudBits']}}",
                    f"{str(Fila['LongitudHex']):<{Anchuras['LongitudHex']}}",
                    f"{str(Fila['Hash']):<{Anchuras['Hash']}}",
                ]
            )
        )


# imprime las 2 alteraciones del texto con SHA256 y calcula los bits distintos entre ambos hashes
def MostrarCambioBitsSha256() -> None:
    HashUno = CalcularHashTexto("MediSoft-v2.1.0", "SHA256")
    HashDos = CalcularHashTexto("medisoft-v2.1.0", "SHA256")
    BitsDistintos = CalcularBitsDistintosHex(HashUno, HashDos)
    print()
    print(f"BitsDistintosSHA256: {BitsDistintos}")


# función principal
def main() -> None:
    Filas = ConstruirFilas()
    ImprimirTabla(Filas)
    MostrarCambioBitsSha256()


if __name__ == "__main__":
    main()
