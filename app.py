from flask import Flask, render_template, request, jsonify
import threading
import time
import random
import sqlite3
import atexit
import os
from ai_analysis import generate_analysis


app = Flask(__name__)

DB_PATH = os.path.join("instance", "data.db")
generator_thread = None
generator_running = False


def generate_data():
    """Background function to simulate data generation."""
    global generator_running

    os.makedirs("instance", exist_ok=True)
    while generator_running:
        try:
            # open connection inside loop to ensure new handle each iteration
            conn = sqlite3.connect(DB_PATH, check_same_thread=False)
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sensor_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    temperature REAL,
                    pressure REAL,
                    flow REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            temp = round(random.uniform(35, 50), 2)
            pressure = round(random.uniform(900, 1000), 2)
            flow = round(random.uniform(10, 60), 2)
            cur.execute(
                "INSERT INTO sensor_data (temperature, pressure, flow) VALUES (?, ?, ?)",
                (temp, pressure, flow)
            )
            conn.commit()
            print(f"Inserted new data: {temp}°C, {pressure}hPa, {flow} L/s")

        except Exception as e:
            print("❌ Data generation error:", e)
        finally:
            conn.close()

        time.sleep(6)   

    print("✅ Background generator exited cleanly.")


def start_data_generation():

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🧹 Old database cleared for new session.")


    """Start the background generator if not already running."""
    global generator_thread, generator_running
    if generator_thread is None or not generator_thread.is_alive():
        generator_running = True
        generator_thread = threading.Thread(target=generate_data, daemon=True)
        generator_thread.start()
        print("🟢 Background data generator started.")
    else:
        print("⚠️ Generator already running, skipping.")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    global generator_running
    if not generator_running:
        print("♻️ Restarting data generator...")
        start_data_generation()
    else:
        print("⚙️ Generator already active.")
    return render_template('dashboard.html')




@app.route('/data')
def get_data():
    """Return latest 25 sensor readings as JSON for dashboard charts."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, temperature, pressure, flow FROM sensor_data ORDER BY id DESC LIMIT 25")
    rows = cur.fetchall()
    conn.close()

    data = {
        "timestamps": [r[0] for r in rows][::-1],
        "temperature": [r[1] for r in rows][::-1],
        "pressure": [r[2] for r in rows][::-1],
        "flow": [r[3] for r in rows][::-1],
    }
    return jsonify(data)


@app.route('/analyze', methods=['GET'])
def analyze_data():
    """Fetch recent sensor readings and generate AI summary."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT temperature, pressure, flow FROM sensor_data ORDER BY id DESC LIMIT 25")
    rows = cur.fetchall()
    conn.close()

    if not rows:
        return jsonify({"analysis": "No data available for analysis."})

    latest_data = {
        "temperature": [r[0] for r in rows][::-1],
        "pressure": [r[1] for r in rows][::-1],
        "flow": [r[2] for r in rows][::-1],
    }

    summary = generate_analysis(latest_data)
    return jsonify({"analysis": summary})




@app.route('/stop', methods=['POST'])
def stop_generation():
    """Stop data generation cleanly but don't delete DB."""
    global generator_running
    generator_running = False
    print("🛑 Data generation paused (DB retained).")
    return jsonify({"status": "stopped"})



def cleanup():
    """Cleanup when Flask shuts down."""
    global generator_running
    generator_running = False
    print("🛑 Cleaning up before shutdown...")

    time.sleep(2)
    try:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("🧼 Database deleted on shutdown.")
    except Exception as e:
        print("⚠️ Cleanup failed:", e)


atexit.register(cleanup)

if __name__ == '__main__':
    app.run(debug=True)