from flask import Flask
import os
import sys

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this


# ---- AUTH_DIR setup ----
AUTH_DIR = os.environ.get("AUTH_DIR")
if not AUTH_DIR:
    raise RuntimeError("AUTH_DIR not set")

if AUTH_DIR not in sys.path:
    sys.path.insert(0, AUTH_DIR)
import auth

authenticate = auth.authenticate
# import routes AFTER app is created
import login
import dashboard
import mbookings

login.register(app)
dashboard.register(app)
# mbookings.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
