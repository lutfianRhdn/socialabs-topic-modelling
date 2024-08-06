from multiprocessing import Process
from consumer import start_consumer
from app import start_app
import os
import subprocess

def start_app():

    # if os windows not run with gunicorn
    subprocess.run(["gunicorn", "--config", "gunicorn_config.py", "app:app"])

def main():
    # Start the consumer process
    p1 = Process(target=start_consumer)
    
    # Start the Flask application process using Gunicorn
    p2 = Process(target=start_app)
    
    # Start both processes
    p1.start()
    p2.start()
    
    # Wait for both processes to complete
    p1.join()
    p2.join()

if __name__ == '__main__':
    main()
