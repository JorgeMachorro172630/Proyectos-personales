# Sistema de Registro de Asistencia con Códigos de Barras

## Descripción
Este script de Python lee el puerto COM donde está conectado el lector GM65 (que funciona en modo HID como dispositivo de entrada tipo teclado). Cuando el lector escanea un código de barras (por ejemplo, de una credencial estudiantil o de profesor), el sistema:

1. Busca coincidencias en la base de datos (archivo Excel con información de usuarios)
2. Registra en la terminal de Visual Studio Code:
   - **Primer escaneo**: Marca hora de entrada
   - **Segundo escaneo**: Registra hora de salida en la base de datos
3. Actualiza automáticamente el registro de asistencia

## Hardware Utilizado
- Arduino UNO
- Lector de códigos de barras GM65 (conectado vía USB)
- Pantalla LCD 16x2 con interfaz I2C
- Cables de conexión (jumpers)


