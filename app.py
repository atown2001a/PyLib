from flask import Flask

app = Flask(__name__)
app.secret_key = "your_secret_key"  # change this

# import routes AFTER app is created
import login
import dashboard
import mbookings

login.register(app)
dashboard.register(app)
#mbookings.register(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
