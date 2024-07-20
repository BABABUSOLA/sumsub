# from app import app

# if __name__ == '__main__':
#     app.run(debug=True, port=8080)


# from flask import Flask

# from app import routes

# app = Flask(__name__)

# # Register the blueprint
# app.register_blueprint(routes.routes)

# if __name__ == '__main__':
#     app.run(debug=True)
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
