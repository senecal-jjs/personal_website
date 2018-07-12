from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

p = Post(body="An exploration of tree search in game playing AI's.", 
         title="MiniMax & Game Playing AI")