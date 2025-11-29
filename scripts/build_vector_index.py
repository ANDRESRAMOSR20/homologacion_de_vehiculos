import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.vector_store.build_index import build_index

if __name__ == "__main__":
    build_index()
