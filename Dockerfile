# For Python 3.4
FROM       python:3.4.2

WORKDIR    /var/app

RUN        pip3 install virtualenv
RUN        virtualenv /var/app
RUN        /var/app/bin/pip install uwsgi
RUN        pip3 install awscli
RUN        useradd uwsgi -s /bin/false
RUN        mkdir /var/log/uwsgi
RUN        chown -R uwsgi:uwsgi /var/log/uwsgi
RUN        apt-get update && apt-get install -y npm node
RUN        npm install -g bower


ADD        . /var/app
RUN        if [ -f /var/app/requirements.txt ]; then /var/app/bin/pip install -r /var/app/requirements.txt; fi

ENV        UWSGI_NUM_PROCESSES    1
ENV        UWSGI_NUM_THREADS      15
ENV        UWSGI_UID              uwsgi
ENV        UWSGI_GID              uwsgi
ENV        UWSGI_LOG_FILE         /var/log/uwsgi/uwsgi.log

EXPOSE     8080

ADD        uwsgi-start.sh /
ADD        app_start.sh /

CMD        []
ENTRYPOINT ["/app_start.sh"]