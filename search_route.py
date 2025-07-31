import pandas as pd
import requests
import json
import io

# URL endpoint server Valhalla lokal Anda
VALHALLA_URL = "http://localhost:8002/route"

# Data koordinat Anda.
# Jika data ada di file CSV, Anda bisa memuatnya dengan:
# df = pd.read_csv('nama_file_anda.csv')
# Di sini kita buat DataFrame dari data gambar Anda.
data = """
BRANCH_LONGITUDE,BRANCH_LATITUDE,SELECTED_LONGITUDE,SELECTED_LATITUDE
106.89933,-6.1642,106.91148,-6.16702
120.31,-4.55015,120.38229,-4.5337
104.06778,-4.55727,104.1022,-4.57383
107.01986,-6.30182,107.03473,-6.29907
"""
df = pd.read_csv(io.StringIO(data))

def get_route_distance(start_lon, start_lat, end_lon, end_lat):
    """
    Mengirim permintaan ke Valhalla untuk mendapatkan jarak dan durasi rute.
    """
    # Struktur payload JSON untuk permintaan Valhalla
    payload = {
        "locations": [
            {"lat": start_lat, "lon": start_lon},
            {"lat": end_lat, "lon": end_lon}
        ],
        "costing": "auto",  # Opsi costing: auto, truck, pedestrian, bicycle
        "units": "kilometers" # Opsi unit: kilometers atau miles
    }

    headers = {'Content-type': 'application/json'}

    try:
        response = requests.post(VALHALLA_URL, data=json.dumps(payload), headers=headers, timeout=30)
        
        if response.status_code == 200:
            route_info = response.json()
            # Ekstrak ringkasan perjalanan dari respons
            summary = route_info.get('trip', {}).get('summary', {})
            distance_km = summary.get('length') # dalam kilometer
            duration_min = summary.get('time') / 60 # dalam menit
            return distance_km, duration_min
        else:
            print(f"Error dari server Valhalla: {response.status_code} - {response.text}")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"Gagal terhubung ke server Valhalla: {e}")
        return None, None

# Iterasi setiap baris di DataFrame untuk menghitung jarak
for index, row in df.iterrows():
    print(f"--- Menghitung Rute #{index + 1} ---")
    
    start_point = (row['BRANCH_LONGITUDE'], row['BRANCH_LATITUDE'])
    end_point = (row['SELECTED_LONGITUDE'], row['SELECTED_LATITUDE'])

    print(f"Dari: {start_point} ke: {end_point}")
    
    distance, duration = get_route_distance(
        start_lon=start_point[0],
        start_lat=start_point[1],
        end_lon=end_point[0],
        end_lat=end_point[1]
    )

    if distance is not None and duration is not None:
        print(f"✅ Hasil: Jarak = {distance:.2f} km, Perkiraan Durasi = {duration:.2f} menit")
    else:
        print("❌ Gagal mendapatkan rute.")
    print("-" * 25)