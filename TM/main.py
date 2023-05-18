from time import sleep

from app.server import TMServer
from app.config import qb_python, qb_c

host = "localhost"
port = 8080


tm = TMServer(host, port, qb_python, qb_c)
tm.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt sent.")
        tm.shutdown()
        exit(0)
    except Exception:
        exit(0)
