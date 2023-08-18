FROM python:3.11-bookworm

WORKDIR /app
RUN apt update && apt install -y nginx
RUN pip3 install supervisor

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY conf/nginx.conf /etc/nginx/sites-available/
RUN rm -rf /etc/nginx/sites-enabled/* 
RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf 

COPY conf/supervisord.conf /etc/supervisord.conf

RUN python3 manage.py create_db

# copy project
COPY . .

EXPOSE 9000
CMD ["/usr/local/bin/supervisord"]
