# [Choice] Ubuntu version (use ubuntu-22.04 or ubuntu-18.04 on local arm64/Apple Silicon): ubuntu-22.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT=ubuntu-22.04
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libbz2-dev \
    libdb-dev \
    libreadline-dev \
    libffi-dev \
    libgdbm-dev \
    liblzma-dev \
    libncursesw5-dev \
    libsqlite3-dev \
    libssl-dev \
    zlib1g-dev \
    uuid-dev \
    bat \
    curl \
    exa \
    fish \
    make \
    ripgrep \
    wget \
 && rm -rf /var/lib/apt/lists/*

# Install Starship
RUN curl -sS https://starship.rs/install.sh | sh -s -- --yes

# Install Python and pip
ARG PYTHON_VERSION=3.10.6
RUN curl -Lo python.tgz "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz" && \
    mkdir -p /usr/src/python && \
    tar --extract --directory /usr/src/python/ --strip-components 1 --file python.tgz && \
    rm python.tgz && cd /usr/src/python && \
    ./configure --enable-optimizations && make altinstall
RUN cd /usr/local/bin && ln -fs idle3 idle && ln -fs pydoc3 pydoc && ln -fs python3.10 python && ln -fs python3.10-config python-config
RUN curl -kL https://bootstrap.pypa.io/get-pip.py | python

# Install Poetry
COPY ./pyproject.toml ./poetry.lock ./
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

WORKDIR /app

USER vscode
