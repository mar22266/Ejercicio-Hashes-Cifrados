# Ejercicio Hashes y Firma Digital

## Descripcion

Este ejercicio implementa dos capas de proteccion. La primera capa protege la integridad de paquetes distribuidos mediante manifiestos SHA256. La segunda capa es la autenticacion de usuarios al mostrar hashes de contrasenas y consultar si esas contrasenas aparecieron en filtraciones conocidas usando Have I Been Pwned con k anonymity. Adicionalmente, el manifiesto se protege con firma digital RSA para aportar autenticidad y evitar que un atacante pueda modificar el archivo `SHA256SUMS.txt` sin ser detectado.

## Instalacion

### Windows

```bash
py -3.14 -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

## Uso

Comandos:

```bash
python src/explorarHashes.py
python src/consultarHibp.py
python src/generarManifiesto.py datosPrueba/archivo1.txt datosPrueba/archivo2.txt datosPrueba/archivo3.txt datosPrueba/archivo4.txt datosPrueba/archivo5.txt
python src/verificarPaquete.py
python src/generarClavesRsa.py
python src/firmarManifiesto.py
python src/verificarFirma.py
```

### Las respuestas a las preguntas de analisis van dentro del incisio que le corresponde

## Inciso 1 Comparacion de algoritmos

Script:

```bash
python src/explorarHashes.py
```

Ejemplo de Ejecucion:

```text
Texto           | Algoritmo | LongitudBits | LongitudHex | Hash
--------------- | --------- | ------------ | ----------- | ----------------------------------------------------------------
MediSoft-v2.1.0 | MD5       | 128          | 32          | cac2fe40370e3a68f0a4927c20c75c89
medisoft-v2.1.0 | MD5       | 128          | 32          | fa386a0d796e388b24cb3302c185a445
MediSoft-v2.1.0 | SHA1      | 160          | 40          | 3ab92abc44e23465b154e887f90c3a5e0d642c65
medisoft-v2.1.0 | SHA1      | 160          | 40          | 4fe9fa8c97db362ecce61ee6302a92f0505217cd
MediSoft-v2.1.0 | SHA256    | 256          | 64          | 64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996
medisoft-v2.1.0 | SHA256    | 256          | 64          | ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e
MediSoft-v2.1.0 | SHA3_256  | 256          | 64          | 3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2
medisoft-v2.1.0 | SHA3_256  | 256          | 64          | 569daf2d0645c0ab6c0a7960cb552f28ac1a222284fa5605ab11cfe0a2dce82c

BitsDistintosSHA256: 120
```

Un cambio pequeno en la entrada produce una salida muy diferente en el hash.
MD5 no es adecuado para integridad de archivos porque tiene 128 bits y ademas existen colisiones conocidas.

### Preguntas y Respuestas

¿Cuántos bits cambiaron entre los dos hashes SHA-256? Usen XOR para contarlos. ¿Qué propiedad demuestra esto?

- En esta ejecucion cambiaron 120 bits. El valor depende del resultado calculado por el script para las entradas comparadas. Esto demuestra que donde un cambio minimo en la entrada provoca muchos cambios en la salida.

Con base en la longitud en bits, explica por qué MD5 es considerado inseguro para integridad de archivos

- MD5 produce hashes de 128 bits, lo que ya da menos margen de seguridad que algoritmos mas modernos. Ademas, existen colisiones, por lo que un atacante puede construir archivos distintos con el mismo hash y romper la confianza en la verificacion de integridad.

## Inciso 2 Consulta HIBP

Script:

```bash
python src/consultarHibp.py
```

Ejemplo de Ejecucion:

```text
Contrasena: admin
SHA256: 8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918
SHA1: D033E22AE348AEB5660FC2140AEC35850C4DA997
PrefijoEnviado: D033E
Nota: solo se envia el prefijo SHA1 de 5 caracteres, nunca el hash completo.
AparicionesFiltraciones: 42085691
--------------------------------------------------------------------------------
Contrasena: 123456
SHA256: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
SHA1: 7C4A8D09CA3762AF61E59520943DC26494F8941B
PrefijoEnviado: 7C4A8
Nota: solo se envia el prefijo SHA1 de 5 caracteres, nunca el hash completo.
AparicionesFiltraciones: 209972844
--------------------------------------------------------------------------------
Contrasena: hospital
SHA256: 8afe3c83decffdf6dc48597a3f1a52be7c6e2b97b4bdf3b15e20a87a1f657f01
SHA1: 2B2D005E88CE14A4112785BB266B2C0C16BE7EB4
PrefijoEnviado: 2B2D0
Nota: solo se envia el prefijo SHA1 de 5 caracteres, nunca el hash completo.
AparicionesFiltraciones: 118791
--------------------------------------------------------------------------------
Contrasena: medisoft2024
SHA256: 78c12e8e24dfd7836c748c33dff2e9150c028d69488f203485e13f4a6daa777c
SHA1: F80CF41ABF90CAA2EC08527F641C40B4ABFE4DB9
PrefijoEnviado: F80CF
Nota: solo se envia el prefijo SHA1 de 5 caracteres, nunca el hash completo.
AparicionesFiltraciones: 0
--------------------------------------------------------------------------------
```

calcula SHA256 para mostrarlo en consola y calcula SHA1 en mayusculas para la consulta a HIBP. se envian solo los primeros 5 caracteres del SHA1 a https://api.pwnedpasswords.com/range/{primeros5}, busca la coincidencia y muestra el numero de apariciones o 0.

## Inciso 3 Verificacion de integridad

### Generar manifiesto

```bash
python src/generarManifiesto.py datosPrueba/archivo1.txt datosPrueba/archivo2.txt datosPrueba/archivo3.txt datosPrueba/archivo4.txt datosPrueba/archivo5.txt
```

Ejemplo de Ejecucion:

```text
ArchivosProcesados: 5
```

Se guarda en el txt y el txt contiene:

```text
8ef8b4119494dda68e8d787901bd82803f8a9ede9b8848984cfcbfcfc0e4cea3 datosPrueba/archivo1.txt
0f98528576c8a01b9b13584d8a0bbf80b3f319baf3edd4584c1096c6997bdde8 datosPrueba/archivo2.txt
11edd4c27c84fe6a5eaed05bc0c29585cf1be2248de14bfa1c232be65c963e74 datosPrueba/archivo3.txt
d88935f23f77376756eaed0d5575be3795b070c4a5a836d9d619b9c7a7e79041 datosPrueba/archivo4.txt
27e4314d2375cb9bc3757619b5ee9cb2679979fb2a9173b9aaf520c1b88af8d2 datosPrueba/archivo5.txt
```

Se guardan los hashes para cada txt en un solo archivo por linea.

### Verificar paquete

```bash
python src/verificarPaquete.py
```

Ejemplo de Ejecucion:

```text
Archivo: datosPrueba/archivo1.txt
HashEsperado: 8ef8b4119494dda68e8d787901bd82803f8a9ede9b8848984cfcbfcfc0e4cea3
HashActual: 8ef8b4119494dda68e8d787901bd82803f8a9ede9b8848984cfcbfcfc0e4cea3
Estado: Correcto
--------------------------------------------------------------------------------
Archivo: datosPrueba/archivo2.txt
HashEsperado: 0f98528576c8a01b9b13584d8a0bbf80b3f319baf3edd4584c1096c6997bdde8
HashActual: 0f98528576c8a01b9b13584d8a0bbf80b3f319baf3edd4584c1096c6997bdde8
Estado: Correcto
--------------------------------------------------------------------------------
Archivo: datosPrueba/archivo3.txt
HashEsperado: 11edd4c27c84fe6a5eaed05bc0c29585cf1be2248de14bfa1c232be65c963e74
HashActual: 11edd4c27c84fe6a5eaed05bc0c29585cf1be2248de14bfa1c232be65c963e74
Estado: Correcto
--------------------------------------------------------------------------------
Archivo: datosPrueba/archivo4.txt
HashEsperado: d88935f23f77376756eaed0d5575be3795b070c4a5a836d9d619b9c7a7e79041
HashActual: d88935f23f77376756eaed0d5575be3795b070c4a5a836d9d619b9c7a7e79041
Estado: Correcto
--------------------------------------------------------------------------------
Archivo: datosPrueba/archivo5.txt
HashEsperado: 27e4314d2375cb9bc3757619b5ee9cb2679979fb2a9173b9aaf520c1b88af8d2
HashActual: 27e4314d2375cb9bc3757619b5ee9cb2679979fb2a9173b9aaf520c1b88af8d2
Estado: Correcto
--------------------------------------------------------------------------------
TotalArchivos: 5
Correctos: 5
Alterados: 0
```

Ejemplo de salida cuando un archivo fue alterado solo se le cambio una letra:

```text
Archivo: datosPrueba/archivo1.txt
HashEsperado: 8ef8b4119494dda68e8d787901bd82803f8a9ede9b8848984cfcbfcfc0e4cee3
HashActual: 8ef8b4119494dda68e8d787901bd82803f8a9ede9b8848984cfcbfcfc0e4cea3
Estado: Alterado
--------------------------------------------------------------------------------
```

Se verifica la integridad del archivo y que no haya sido editado a traves del hash

## Inciso 4 Generacion de claves y firma

### Generar claves RSA

```bash
python src/generarClavesRsa.py
```

Se genera la llave privada y publica

Ejemplo de Ejecucion:

```text
Clave privada generada en: C:/Users/xxx/xxx/Desktop/Ejercicio-Hashes-Cifrados/salidas/medisoftPriv.pem
Clave publica generada en: C:/Users/xxx/xxx/Desktop/Ejercicio-Hashes-Cifrados/salidas/medisoftPub.pem
```

### Firmar manifiesto

```bash
python src/firmarManifiesto.py
```

Ejemplo de Ejecucion:

```text
Firma generada en: C:/Users/xxx/xxx/Desktop/Ejercicio-Hashes-Cifrados/salidas/SHA256SUMS.sig
```

## Inciso 5 Verificacion de autenticidad

Script:

```bash
python src/verificarFirma.py
```

Experimento 1:
Al Cambiar un solo caracter del archivo.

Resultado:

```text
Firma invalida
```

Experimento 2:
Al Cambiar un byte de `datosPrueba/archivo3.txt`. Luego correr `python src/verificarFirma.py`. La salida sigue siendo `Firma valida` porque el manifiesto firmado no cambio.
Luego se corre `python src/verificarPaquete.py` y observe que ese archivo aparece como `Alterado`.
Resultado verificar firma

```text
Firma valida
```

Resultado Verificar paquete

```text
--------------------------------------------------------------------------------
Archivo: datosPrueba/archivo4.txt
HashEsperado: d88935f23f77376756eaed0d5575be3795b070c4a5a836d9d619b9c7a7e79041
HashActual: 63ff9cba406a01a2682ea478c25496dbb31765a796483c1223f38895decb91d6
Estado: Alterado
--------------------------------------------------------------------------------
```

Pregunta: Porque la firma es valida? Que sucede al ejecutar verificar_paquete.py
Respuesta:

La firma es valida cuando solo se altera un archivo de datos pero no el manifiesto porque la firma protege exclusivamente el contenido del manifiesto firmado.
A la hora de correr `src/verificarPaquete.py` en ese escenario, la verificacion de integridad falla para el archivo alterado porque su hash actual ya no coincide con el hash esperado en `SHA256SUMS.txt`.

## Referencias bibliograficas

- Python Software Foundation. `hashlib` - Secure hashes and message digests. [https://docs.python.org/3/library/hashlib.html](https://docs.python.org/3/library/hashlib.html)

- Have I Been Pwned. Pwned Passwords API. [https://haveibeenpwned.com/API/v3#PwnedPasswords](https://haveibeenpwned.com/API/v3#PwnedPasswords)

- PyCryptodome Documentation. Public key RSA. [https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html](https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html)

- PyCryptodome Documentation. PKCS#1 v1.5 signature. [https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html](https://pycryptodome.readthedocs.io/en/latest/src/signature/pkcs1_v1_5.html)

- OpenAI. (2026). ChatGPT. Retrieved March 20, 2026, from https://openai.com/chatgpt/overview/
