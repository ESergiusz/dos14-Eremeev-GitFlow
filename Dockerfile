FROM python:3.11.3-buster
ARG APP_FOLDER=app
ARG USER_NAME=authz
ARG USER_ID=1983
RUN useradd -d /home/$USER_NAME -U -m -u $USER_ID $USER_NAME && mkdir /home/$USER_NAME/$APP_FOLDER
RUN pip install --upgrade pip && pip install poetry && chmod 755 /home/$USER_NAME/$APP_FOLDER
#RUN  chmod 666 /var/run/docker.sock
WORKDIR /home/$USER_NAME/git
USER $USER_NAME
COPY --chown=$USER_NAME:$USER_NAME users.json roles.yaml pyproject.toml poetry.lock main.py app.yaml /home/$USER_NAME/$APP_FOLDER/
WORKDIR /home/$USER_NAME/$APP_FOLDER
RUN poetry install
ENTRYPOINT ["poetry","run","python","main.py"]