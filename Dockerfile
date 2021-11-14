FROM python:3.5-alpine3.10
COPY . /todo
WORKDIR /todo
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]