import os
from FRA import app

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
