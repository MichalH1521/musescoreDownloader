from app import create_app
from dotenv import load_dotenv
import os

load_dotenv()

app = create_app()

envir = os.getenv('FLASK_ENV', None)
debug = True
if envir == "production":
    debug = False
else:
    debug = True
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000), debug=debug)
