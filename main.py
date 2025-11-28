import time
import serial
from supabase import create_client, Client  # pip install supabase

# --- CONFIGURACIÓN SUPABASE (EN TEXTO CLARO) ---
SUPABASE_URL = "https://qjzjxcjcfjfammkyskpx.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFqemp4Y2pjZmpmYW1ta3lza3B4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk1NDk5MTMsImV4cCI6MjA3NTEyNTkxM30.dZUMwvYN_0ILfGDLK1ELneBQz-D-NCb_c6_hprESdDg"  # clave anon o service_role según el uso

# --- CONFIGURACIÓN SERIE ---
# En Raspberry suele ser "/dev/ttyACM0" o "/dev/ttyUSB0"
# En Windows, algo como "COM3", "COM4", etc.
SERIAL_PORT = "/dev/ttyACM0"
BAUDRATE = 115200

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def read_measurement(ser: serial.Serial):
    """
    Lee una línea del Arduino y la convierte en un dict listo para Supabase.
    Formato esperado: ph,temp_c,ph_alarm,tds_ppm,humedad_pct
    Ejemplo: 7.01,23.45,0,250.12,63
    """
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if not line:
        return None

    parts = [p.strip() for p in line.split(",")]
    if len(parts) != 5:
        print("Línea con formato inesperado:", line)
        return None

    ph_str, temp_str, alarm_str, tds_str, hum_str = parts

    try:
        return {
            "id": "pablo",                     # campo id fijo
            "ph": float(ph_str),
            "temp_c": float(temp_str),
            "ph_alarm": bool(int(alarm_str)),  # 0/1 -> False/True
            "tds_ppm": float(tds_str),
            "humedad_pct": float(hum_str),
        }
    except ValueError:
        print("No se pudo convertir la línea:", line)
        return None

def main():
    print("Abriendo puerto serie", SERIAL_PORT)
    ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=20)
    # Pequeña espera para que el Arduino se reinicie
    time.sleep(2)

    print("Conectando a Supabase:", SUPABASE_URL)
    # Inserción de prueba mínima para comprobar conexión (opcional):
    # supabase.table("data_sensor").insert({"id": "pablo"}).execute()

    print("Escuchando datos del Arduino...")
    while True:
        data = read_measurement(ser)
        if data:
            try:
                res = supabase.table("data_sensor").insert(data).execute()
                print("Insertado en Supabase:", data)
            except Exception as e:
                print("Error al insertar en Supabase:", e)
        else:
            print("Sin dato válido en este ciclo")

        # El Arduino ya envía solo una línea por minuto; no hace falta dormir más
        # pero este pequeño sleep evita que el bucle se dispare si algo va mal.
        time.sleep(0.5)

if __name__ == "__main__":
    main()
