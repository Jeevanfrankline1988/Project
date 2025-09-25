from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    return jsonify(status="ok"), 200

if __name__ == "__main__":
    # Debug only for local dev, never in production
    app.run(host="0.0.0.0", port=5000, debug=True)
