# ██████╗ ██╗   ██╗██╗██╗     ██████╗ 
# ██╔══██╗██║   ██║██║██║     ██╔══██╗
# ██████╔╝██║   ██║██║██║     ██║  ██║
# ██╔══██╗██║   ██║██║██║     ██║  ██║
# ██████╔╝╚██████╔╝██║███████╗██████╔╝
# ╚═════╝  ╚═════╝ ╚═╝╚══════╝╚═════╝  Step

# https://hub.docker.com/_/python
FROM python:3.9-slim
RUN apt update && apt install -y  postgresql-client netcat build-essential musl-dev zlib1g-dev libjpeg-dev libpq-dev postgresql-client locales
RUN locale-gen es_PE.UTF-8 && localedef -i es_PE -c -f UTF-8 -A /usr/share/locale/locale.alias es_PE.UTF-8

# Set base Python Environment Variables
ENV LANG es_PE.UTF-8
ENV LANGUAGE es_PE:es
ENV LC_ALL es_PE.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DB_TYPE postgres

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Remove extra libraries
RUN apt remove -y build-essential musl-dev && apt-get remove --purge --auto-remove -y

# Expose 80
EXPOSE 80

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--chdir", "/app", "core.wsgi"]
