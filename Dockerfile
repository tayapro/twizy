FROM ubuntu:jammy

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*]

RUN python3 -m pip install --no-cache-dir --upgrade \
    setuptools wheel virtualenv pipenv pylint rope flake8 \
    mypy autopep8 pep8 pylama pydocstyle bandit notebook \
    twine

COPY components/ components/
COPY config/ config/
COPY controllers/ controllers/
COPY lib/ lib/
COPY screens/ screens/
COPY static/ static/
COPY views/ views/
COPY requirements.txt .
COPY package.json .
COPY index.js .
COPY run.py .
COPY creds.json .

RUN python3 -m pip install -r requirements.txt

# Install NVM and Node.js
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

ENV NVM_DIR=/root/.nvm
ENV PATH=$NVM_DIR/versions/node/v16.13.0/bin:$PATH

RUN bash -c "source $NVM_DIR/nvm.sh \
    && nvm install 16.13.0 \
    && nvm use 16.13.0 \
    && nvm alias default 16.13.0"

RUN npm install

CMD ["node", "index.js"]
