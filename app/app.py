from flask import Flask
import os

app = Flask(__name__)

@app.get("/")
def home():
    name = os.getenv("APP_NAME", "k8s-argocd-lab")
    env = os.getenv("APP_ENV", "dev")
    return {"app": name, "env": env, "message": "Hello from Kubernetes + Argo CD!"}

@app.get("/healthzyyyyyy")
def healthz():
    return "ok", 200

@app.get("/readyyyyyyy")
def readyz():
    return "ready", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
