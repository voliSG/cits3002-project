from time import sleep

from app.server import TMServer

host = "localhost"
port = 8080

tm = TMServer(host, port)
tm.start()

while True:
    try:
        sleep(1)
    except KeyboardInterrupt:
        print("Keyboard Interrupt sent.")
        tm.shutdown()
        exit(0)
