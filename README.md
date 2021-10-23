
# ThisPc-API

![python --version](https://img.shields.io/badge/python-3.6%7C3.7%7C3.8-green)

ThisPc-Api is a Redis publisher, and an API endpoint used in [ThisPc project](https://github.com/Goldenboycoder/this-pc-project), to deliver performance and system resources data about this pc.
## Appendix
[ThisPC-Project](https://github.com/Goldenboycoder/this-pc-project)

[ThisPC-Client](https://github.com/Goldenboycoder/this-pc-client): installed on the PC to monitor with.

## Features

- Collect: CPU, Memory, Network IO and Storage Disks stats.
- API endpoint: Using FastAPI this pc becomes an API endpoint allowing remote entities to query the collected data about system resources, performance and running processes.
- Interactive API documentation thanks to FastAPI automatic docs generation (OpenAPI).
- Redis Publisher: This pc regularly publishes its collected data under a Redis channel PC-<PcName> which enables subscribers to the PC-* pattern to get live data.

  
## Installation

Clone this repository

```cmd
  git clone https://github.com/Goldenboycoder/this-pc-api.git
  cd this-pc-api
```

## Dependencies

```
pip install fastapi
pip install "uvicorn[standard]"
pip install "uvicorn[standard]" gunicorn
pip install redis
```
## Usage

Depending on your environment you can use one of the following:

If running on Windows OS, use the ASGI server uvicorn which runs in a single process:

```python deploy.py -m uvicorn ```

If running on Linux, then use [gunicorn](https://fastapi.tiangolo.com/deployment/server-workers/#gunicorn-with-uvicorn-workers) as a process manager in addition to uvicorn worker processes.

```python deploy.py -m gunicorn```


  
## Interactive API docs

Open your browser to: [127.0.0.1:5555/docs](127.0.0.1:5555/docs)

You will see the automatic interactive API documentation (provided by [Swagger UI](https://github.com/swagger-api/swagger-ui))
The docs get automatically updated as you change the API.

![Docs](https://github.com/Goldenboycoder/this-pc-project/blob/main/imgs/docs.png)

## Alternative API docs
Go to: [127.0.0.1:5555/redocs](127.0.0.1:5555/redocs)

You will see the alternative automatic documentation (provided by [ReDoc](https://github.com/Rebilly/ReDoc))

![Redoc](https://github.com/Goldenboycoder/this-pc-project/blob/main/imgs/redoc.png)

*N.B: Port number may be different if you changed it.*

  
## License

[BSD 3-Clause License](./LICENSE)

  
## Author

- [@Patrick Balian](https://github.com/Goldenboycoder)

[![twitter](https://img.shields.io/twitter/follow/patrick_balian?style=social)](https://twitter.com/Patrick_Balian)

[![linkedin](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/patrick-balian-41b851147/)
