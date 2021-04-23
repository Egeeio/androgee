FROM python:3.9-buster
RUN mkdir /app
# mount /app/configs and place badwords.json in the folder you have badwords.json in
COPY configs /app/configs/  
COPY androgee /app/androgee
COPY poetry.lock /app
COPY pyproject.toml /app
RUN apt update && apt upgrade -y
RUN pip3 install poetry
WORKDIR /app
RUN poetry install
ENTRYPOINT [ "/usr/local/bin/poetry", "run", "start"]