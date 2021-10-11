import config as Settings
import sys , getopt
import uvicorn
import os
from producer import Producer
import threading

def main(argv):
    '''
    cmd : gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    to run with process manager
    '''
    manager = ""
    try:
        opts ,args = getopt.getopt(argv,"hm:",["manager"])
    except getopt.GetoptError:
        print("deploy.py -m <gunicorn/uvicorn>")
    for opt ,arg in opts:
        if opt =='-h':
            print("deploy.py -m <gunicorn/uvicorn>")
            sys.exit()
        elif opt in ("-m","--manager"):
            manager = arg

    if manager == "gunicorn":
        os.system("gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app")
    elif manager == "uvicorn":
        uvicorn.run("main:app", reload = Settings.uvicornReload, port = Settings.serverPort)
    else:
        print("deploy.py -m <gunicorn/uvicorn>")
        sys.exit()


if __name__ == "__main__":
    prod = Producer()
    Settings.producerThread = threading.Thread(target=prod.startProducing,daemon=True)
    main(sys.argv[1:])

