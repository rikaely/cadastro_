from flask import Flask
app = Flask(__name__)
from controllers.cadastro_controller import *
if __name__ == "__main__":
   app.run()




