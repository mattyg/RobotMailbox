# Add app directory to PYTHON PATH
import sys
sys.path.append("")

from app.core import settings
from app.core.controller import Controller

def start():
	ctrl = Controller()

if __name__ == "__main__":
	start()
