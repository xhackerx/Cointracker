from flask import Flask, render_template_string
import os
import sys

sys.path.append(os.path.dirname(__file__))
from alert_service import check_conditions

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<title>Cointracker Alert</title>
<h1>Send Crypto Alert</h1>
<form method="post" action="/send">
    <button type="submit">Check & Send</button>
</form>
{% if result %}
<p>{{ result }}</p>
{% endif %}
"""

@app.route("/")
def index():
    return render_template_string(INDEX_HTML, result=None)

@app.route("/send", methods=["POST"])
def send():
    try:
        check_conditions()
        msg = "Check completed. If conditions met, an email was sent."
    except Exception as exc:  # noqa: BLE001
        msg = f"Error: {exc}"
    return render_template_string(INDEX_HTML, result=msg)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
