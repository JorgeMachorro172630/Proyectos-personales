# Registro de pase de lista

## Descripción
El Script de python lee el puerto COM al que esta conectado el gm65 ya que este esta en mod HID (teclado), al momento de que el GM65 lea algun codigo de barras (por ejemplo de la credencial del estudiante o incluso del maestro) y si esta coincide con la base de datos (en este caso una realizada en excel con la informacion del estudiante o maestro), en la terminal de visual studio code se mostrara un mensaje de la hora de entrada de esa persona, si se vuelve a repetir ese estudiante, lo registra en la base de datos como hora de salida.
## Hardware Usado
- Arduino UNO
- Sensor GM65 (conectado a USB a la laptop)
- Pantalla LCD 16x2 i2C
- Jumpers (Cables)

## Instalación
1. Clona este repositorio.
2. Abre `PantallaLCD.ino` en el IDE de Arduino.
3. Sube el código a tu placa de arduino.
