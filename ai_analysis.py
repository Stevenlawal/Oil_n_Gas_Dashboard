# ai_analysis.py
import os
import openai
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_analysis(latest_data):
    """
    Uses legacy OpenAI API to analyze recent sensor data and return insights.
    """
    try:
        temperature = latest_data["temperature"]
        pressure = latest_data["pressure"]
        flow = latest_data["flow"]

        prompt = f"""
        You are an oil & gas system monitoring assistant.
        Analyze the following sensor readings:
        - Temperature (°C): {temperature[-5:]}
        - Pressure (hPa): {pressure[-10:]}
        - Flow Rate (L/s): {flow[-10:]}

        Generate a short system performance summary, 

        On another paragraph detect two possible anomalies in bullet points,

        and on another paragraph give one actionable suggestion with a bullet point.
        
        Keep it concise and clear for a technical operator.
        Do not add any formatting like trying to make bold or italicising or so on.
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional oil and gas monitoring assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=160,
            temperature=0.6,
        )

        return response["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print("AI analysis error:", e)
        return "⚠️ Unable to generate analysis at the moment."
