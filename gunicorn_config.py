bind = '0.0.0.0:6000'  # Bind to the specified port
workers = 5  # Number of worker processes (recommended: (2 * number of CPUs) + 1)
threads = 2  # Number of threads per worker (adjust based on I/O vs CPU-bound tasks)
accesslog = '-'  # Log access requests to stdout
errorlog = '-'  # Log errors to stdout
