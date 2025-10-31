# 🛢️ Oil & Gas Real-Time Sensor Dashboard

A visually appealing **real-time monitoring dashboard** for simulating and analyzing oil & gas pipeline data using **AI-powered insights**.  
Built with **Flask**, **Chart.js**, and **OpenAI’s API**, it demonstrates data streaming, AI integration, and a clean, responsive front-end interface.

---

## 🚀 Features

- 📊 **Live Data Simulation** – Real-time temperature, pressure, and flow rate visualization.
- ⚠️ **Smart Alerts** – Auto-detects and logs high-pressure readings.
- 🤖 **AI Analysis Panel** – Uses GPT to generate dynamic summaries and performance insights.
- 💎 **Modern UI/UX** – Clean glass-morphism design using Tailwind & Bootstrap.
- 🌐 **Deploy-Ready** – Optimized for Render or any Flask-compatible hosting platform.

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Flask (Python) |
| Frontend | HTML, CSS, Bootstrap 5, TailwindCSS |
| Charts | Chart.js |
| AI Integration | OpenAI API |
| Deployment | Render |
| Data Handling | Fetch API & JSON |

---

## ⚙️ Project Structure

oil-gas-dashboard/
│
├── app.py
├── requirements.txt
├── templates/
│ ├── index.html
│ └── dashboard.html
├── static/
│ └── images/
│ └── image.png
└── .env (not uploaded)


---

## 🧩 Setup Instructions (Local)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/oil-gas-dashboard.git
   cd oil-gas-dashboard

2. **Create a Virtual Environment**

python -m venv venv
source venv/Scripts/activate   # Windows
# or
source venv/bin/activate       # macOS/Linux

3. **Install Dependencies**

pip install -r requirements.txt


4. **Set up Environment Variable**

Create a .env file in the root folder:

OPENAI_API_KEY=your_openai_key_here


5. **Run it**

flask run

Then open: http://127.0.0.1:5000/


**💡 Future Improvements**

🌍 Live IoT device integration instead of simulated data.

📈 Historical data tracking and trend prediction.

🧭 Multi-sensor monitoring dashboard with map visualization.


**👨‍💻 Author**
Stephen Lawal


🪪 License

This project is open-sourced.

⭐ If you like this project, give it a star on GitHub to support future improvements!
