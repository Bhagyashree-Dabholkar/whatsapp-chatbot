from flask import Flask
from routes.whatsapp_routes import whatsapp_bp
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(whatsapp_bp)

if __name__ == '__main__':
    app.run(debug=True)