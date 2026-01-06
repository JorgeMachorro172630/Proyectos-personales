
import keyboard
import pandas as pd
from datetime import datetime
import serial
import time
import os

# Configuración
EXCEL_PATH = r'C:\Users\jlmac\OneDrive\Desktop\python\lista_estudiantes.xlsx'
ARDUINO_PORT = 'COM3' 
COLUMNAS_EXCEL = {
    'nombre': 'Nombre Completo',
    'grupo': 'Grupo',
    'matricula': 'Matricula',
    'entrada': 'Hora de entrada',
    'salida': 'Hora de Salida'
}



buffer = []
registro_activo = {}  

def conectar_arduino():
    try:
        return serial.Serial(ARDUINO_PORT, 9600, timeout=1)
    except serial.SerialException:
        print(f" No se pudo conectar al Arduino en {ARDUINO_PORT}")
        return None

def limpiar_matricula(raw_data):
   
    return ''.join(c for c in raw_data.replace("'", "-").strip() if c.isdigit() or c == '-')

def cargar_excel():
   
    try:
        df = pd.read_excel(EXCEL_PATH)
        
        
        df['Matricula_Num'] = df[COLUMNAS_EXCEL['matricula']].str.extract(r'(\d+)').astype(int)
        df = df.sort_values('Matricula_Num').drop('Matricula_Num', axis=1)
        
        
        columnas_faltantes = [col for col in COLUMNAS_EXCEL.values() if col not in df.columns]
        if columnas_faltantes:
            print(f" Columnas faltantes: {columnas_faltantes}")
            return None
            
        return df
    except Exception as e:
        print(f" Error al cargar Excel: {e}")
        return None

def procesar_matricula(matricula, df, arduino):
   
    hora_actual = datetime.now().strftime('%H:%M:%S')
    matricula = limpiar_matricula(matricula)
    
    
    mask = df[COLUMNAS_EXCEL['matricula']] == matricula
    if not mask.any():
        print(f" Matrícula {matricula} no encontrada")
        return df
        
    idx = mask.idxmax()
    nombre = df.at[idx, COLUMNAS_EXCEL['nombre']]
    
    if matricula not in registro_activo:
        df.at[idx, COLUMNAS_EXCEL['entrada']] = hora_actual
        registro_activo[matricula] = {'entrada': hora_actual}
        mensaje = f" ENTRADA: {nombre} - {hora_actual}"
    else:
        df.at[idx, COLUMNAS_EXCEL['salida']] = hora_actual
        registro_activo.pop(matricula)
        mensaje = f" SALIDA: {nombre} - {hora_actual}"
    
    print(mensaje)
    
    if arduino:
        try:
            arduino.write(f"{matricula}\n".encode())
        except Exception as e:
            print(f" Error al enviar al Arduino: {e}")
    
    return df

def main():
    df = cargar_excel()
    if df is None:
        return
        
    arduino = conectar_arduino()
    context = {'df': df}

    print("\n🔍 Escaneando códigos de barras...")
    print("Presiona ESC para salir\n")

    def on_key(event):
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'enter':
                matricula = ''.join(buffer)
                context['df'] = procesar_matricula(matricula, context['df'], arduino)
                buffer.clear()
                context['df'].to_excel(EXCEL_PATH, index=False)
            else:
                buffer.append(event.name)

    keyboard.hook(on_key)
    keyboard.wait('esc')

    if arduino:
        arduino.close()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n Programa terminado por el usuario")
    finally:
        keyboard.unhook_all()


