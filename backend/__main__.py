from dotenv import load_dotenv

from backend.app import create_app


load_dotenv()

socket, app = create_app()

socket.run(app, host="0.0.0.0", port="8080", debug=True)
