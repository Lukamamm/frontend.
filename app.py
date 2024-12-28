import os
import requests
from flask import Flask, render_template_string

app = Flask(__name__)

BACKENDS = [
    os.getenv("BACKEND_1", ""),
    os.getenv("BACKEND_2", ""),
    os.getenv("BACKEND_3", ""),
]

@app.route('/')
def index():
    statuses = {}
    for i, backend in enumerate(BACKENDS, start=1):
        if backend:
            try:
                response = requests.get(f"{backend}/health", timeout=2)
                if response.status_code == 200:
                    statuses[f"Backend {i}"] = "UP"
                else:
                    statuses[f"Backend {i}"] = "DOWN"
            except requests.exceptions.RequestException:
                statuses[f"Backend {i}"] = "DOWN"
        else:
            statuses[f"Backend {i}"] = "NOT CONFIGURED"

    all_up = all(status == "UP" for status in statuses.values())
    homework_status = (
        "Homework Done Successfully!" if all_up else "Homework is NOT done. Try harder!"
    )
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head><title>Backend Status</title></head>
    <body>
        <h1>Backend Status</h1>
        <ul>
            {% for backend, status in statuses.items() %}
                <li>{{ backend }}: {{ status }}</li>
            {% endfor %}
        </ul>
        <h2>{{ homework_status }}</h2>
    </body>
    </html>
    """, statuses=statuses, homework_status=homework_status)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

