FROM python:3.10

RUN apt-get update && \
    apt-get -y install --no-install-recommends \
    python3-cffi \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    software-properties-common \
    curl \
    npm \
    git \
    git-flow \
    zsh \
    postgresql-client \
    fish && \
    apt-get install -y pre-commit && \
    rm -rf /var/lib/apt/lists/*

# Install pip
RUN pip install --upgrade pip
RUN pip install pre-commit

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_DIR /app
ENV USER app

# Create a non-root user
RUN useradd -ms /bin/bash ${USER}
RUN groupadd -f ${USER}

# Install requirements via requirements.txt
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR ${PROJECT_DIR}

# Chown all the files to the app user
RUN chown -R ${USER}:${USER} .

USER ${USER}

SHELL ["/usr/bin/fish"]

