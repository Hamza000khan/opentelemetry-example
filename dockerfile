FROM python:3.8-slim

COPY requirements.txt /

RUN pip install -r requirements.txt


COPY src /src

WORKDIR /src
# CMD [ "python3", "-m" , "flask", "run", "--port=8000"]
ENTRYPOINT ["bash", "-c", "python -u app.py"]