from app.config import APP_PORT
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=APP_PORT)
