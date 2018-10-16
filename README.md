RUN:
docker run -it     -v /tmp/.X11-unix:/tmp/.X11-unix        -e DISPLAY=$DISPLAY     -u qtuser    page-stats python3 main.py

