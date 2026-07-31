from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>🚀 Cloud CI/CD Platform</h1>
    <h3>Welcome to the Enterprise DevOps Project!</h3>
    <p>This application will be deployed automatically using GitHub Actions.</p>
    """

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "version": "1.0.0"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)