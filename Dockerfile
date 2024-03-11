# Dockerfile

FROM python:3.10

RUN apt-get update

RUN apt-get -y update --fix-missing \
    && apt-get -y install python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    && apt-get -y install software-properties-common curl npm \
    && apt-get -y install git git-flow zsh \
    && apt-get -y install postgresql-client \
    && apt-get install -y pre-commit \
    && apt-get -y install fish
    

ENV PYTHONUNBUFFERED 1

ENV PROJECT_DIR /app
ENV USER app

# Create a non-root user
RUN useradd -ms /bin/bash ${USER}
RUN groupadd -f ${USER}

# Create the project directory and set permissions
RUN mkdir ${PROJECT_DIR}
WORKDIR ${PROJECT_DIR}
RUN chown -R ${USER}:${USER} .

# Switch to root to install system packages
USER root

# Install pre-commit using the system package manager

# Switch back to the non-root user
USER ${USER}

# Copy the rest of the application code
ADD . ${PROJECT_DIR}/

# Install Python dependencies
RUN pip install -r requirements.txt

# Install pre-commit hooks
RUN pip install pre-commit
#RUN pre-commit install

# Set the default shell
SHELL ["/bin/zsh"]

