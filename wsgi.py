import os
import sys

# Add project root to Python path (Crucial for imports)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from webGrabberApi.webGrabberApi import app
