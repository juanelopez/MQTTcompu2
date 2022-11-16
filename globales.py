from concurrent import futures
import queue
hilos = futures.ThreadPoolExecutor()
query_mqtt = queue.Queue()
query_coms = queue.Queue()
guion = "-"