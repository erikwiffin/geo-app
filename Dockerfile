FROM python:3-onbuild
MAINTAINER Erik Wiffin

# Set the environment
ENV FLASK_APP /usr/src/app/app.py

WORKDIR /usr/src/app

ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0"]
