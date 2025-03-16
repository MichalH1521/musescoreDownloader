from flask import Flask, render_template

def create_app():
    app = Flask(__name__)
    app.debug = True
    
    # Load config
    app.config.from_pyfile('config.py')

    # Import and register blueprints (if any)
    from .routes import main
    app.register_blueprint(main)

    return app
