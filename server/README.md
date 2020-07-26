# DL based User Login

## Server Setup

Prerequisite - Python 3.6, Anaconda > 4

### Clone the repository
```
git clone https://github.com/unmesh-shukla/dl_login
```

### Create the virtualenv and install the dependencies
```
cd dl_login/server
conda create -n venv python=3.6
source activate venv
pip install tensorflow-1.3.0-cp36-cp36m-macosx_10_11_x86_64.whl
pip install -r requirements.txt
```
For platforms other than MacOS, download the tensorflow .whl distribution from https://pypi.org/project/tensorflow/1.3.0/#files

### Run database migrations
```
flask db migrate
```

### Run gunicorn to start the app
- For Sync Mode
    ```
    gunicorn --bind 0.0.0.0:5000 start_app:app -w 4 -t 20 --backlog 10000 --log-level=debug
    ```
- For async mode
    ```
    gunicorn --bind 0.0.0.0:5000 --worker-class gevent start_app:app -w 4 -t 20 --backlog 10000 --log-level=debug
    ```

### To load test the app, run locust.
```
locust
```
Open http://localhost:8089 to test the app.


## For production

- Configure Nginx for Server App
    ```
    brew install nginx
    cp nginx.conf /usr/local/etc/nginx/
    cp default /usr/local/etc/nginx/sites-available
    mkdir /usr/local/etc/nginx/sites-enabled
    sudo ln -s /usr/local/etc/nginx/sites-available/default /usr/local/etc/nginx/sites-enabled/
    sudo nginx -t
    sudo nginx -s stop && sudo nginx
    ```

- Redirect the client application to nginx URL - http://0.0.0.0:80
