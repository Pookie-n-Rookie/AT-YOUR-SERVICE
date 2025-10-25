import subprocess
import threading
import time
import requests
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

BACKEND_URL = "http://127.0.0.1:9999/health"  # We'll create a health endpoint in FastAPI

def run_backend():
    try:
        logger.info("Starting backend service...")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", "9999"],
            check=True
        )
    except Exception as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", e)

def wait_for_backend(timeout=30):
    """Wait until the backend is reachable."""
    logger.info("Waiting for backend to be ready...")
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = requests.get(BACKEND_URL)
            if response.status_code == 200:
                logger.info("Backend is ready!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    raise CustomException(f"Backend not reachable after {timeout} seconds")

def run_frontend():
    try:
        logger.info("Starting frontend service...")
        subprocess.run(["streamlit", "run", "app/frontend/ui.py"], check=True)
    except Exception as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", e)

if __name__ == "__main__":
    try:
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=run_backend, daemon=True)
        backend_thread.start()

        # Wait for backend to become ready
        wait_for_backend(timeout=60)

        # Start frontend
        run_frontend()

    except CustomException as e:
        logger.exception(f"CustomException occurred: {str(e)}")
