import os
import time
import pandas as pd
import requests

# -------- CONFIG --------
DATA_DIR = "data"  # مجلد البيانات الرئيسي
API_ENDPOINT = "http://localhost:8501"  # Streamlit app URL
DELAY = 0.05  # تأخير بين كل تحديث بالثواني (يمكن تعديله)

# -------- HELPERS --------
def find_telemetry_files(data_dir):
    telemetry_files = []
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if "telemetry_data.csv" in f:
                telemetry_files.append(os.path.join(root, f))
    return sorted(telemetry_files)

def find_lap_files(data_dir):
    lap_files = []
    for root, dirs, files in os.walk(data_dir):
        for f in files:
            if "_lap_time.csv" in f:
                lap_files.append(os.path.join(root, f))
    return sorted(lap_files)

# -------- LOAD FILES --------
telemetry_files = find_telemetry_files(DATA_DIR)
lap_files = find_lap_files(DATA_DIR)

if not telemetry_files or not lap_files:
    print("[ERROR] No telemetry or lap files found!")
    exit(1)

print(f"[INFO] Found {len(telemetry_files)} telemetry files and {len(lap_files)} lap files.")

# -------- SIMULATION LOOP --------
for t_file, l_file in zip(telemetry_files, lap_files):
    print(f"\n[SIM] Starting simulation for: {t_file}")

    telemetry = pd.read_csv(t_file)
    laps = pd.read_csv(l_file)

    # ترتيب البيانات حسب الزمن
    if "timestamp" in telemetry.columns:
        telemetry = telemetry.sort_values("timestamp")
    else:
        telemetry["timestamp"] = range(len(telemetry))

    # إرسال البيانات
    for i, row in telemetry.iterrows():
        payload = {}
        for col in ["driver", "speed", "lap", "throttle", "brake", "tire_wear", "fuel", "timestamp"]:
            payload[col] = row[col] if col in row else None

        try:
            requests.post(API_ENDPOINT, json=payload)
            print(f"[SIM] {payload.get('driver')} | Lap {payload.get('lap')} | Speed {payload.get('speed')}")
        except Exception as e:
            print("[SIM] ERROR:", e)

        time.sleep(DELAY)

print("[SIM] All simulations finished ✅")
