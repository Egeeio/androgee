FROM python:3.9-buster
RUN mkdir /app
COPY androgee /app/androgee
COPY poetry.lock /app
COPY pyproject.toml /app
RUN apt update && apt upgrade -y
RUN pip3 install poetry
WORKDIR /app
RUN poetry install
ENV DISCORD_PREFIX setthese
ENV DISCORD_TOKEN 
ENV mod_role_id
ENV mod_role_name
ENTRYPOINT [ "/usr/local/bin/poetry", "run", "start"]