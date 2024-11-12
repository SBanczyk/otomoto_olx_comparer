from website import create_app
from os import path, getcwd, getenv
from dotenv import load_dotenv
from website.create_db import create_db


app = create_app()
load_dotenv()


if __name__ == "__main__":
    # if not path.isfile(path.join(getcwd(), getenv('DB_NAME'))):
    create_db()
    app.run(debug=True)
