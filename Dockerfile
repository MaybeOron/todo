FROM python:3.5-alpine3.10
#COPY requirements.txt /todo
#RUN pip install -r requirements.txt
COPY . /todo
ENV MONGODBURL "mongodb://root:root@mongodb:27017/admin"
WORKDIR /todo
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
