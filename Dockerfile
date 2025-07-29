# We use ubuntu becauase we need both nodejs and python and a little bit more.
FROM ubuntu:jammy

WORKDIR /app

# Cherry pick the required files
# Note: We use .dockerignore to avoid files such as *.pyc or __pycache__, etc.
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

# Set up nvm to look at node 16.13 - the minimum LTS required for our project.
ENV NVM_DIR=/root/.nvm
ENV PATH=$NVM_DIR/versions/node/v16.13.0/bin:$PATH

# Install everything in a single docker layer
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* \
    && python3 -m pip install -r requirements.txt \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && bash -c "source $NVM_DIR/nvm.sh \
                && nvm install 16.13.0 \
                && nvm use 16.13.0 \
                && nvm alias default 16.13.0" \
    && npm install

# Expose port (optional)
EXPOSE 8000

CMD ["node", "index.js"]
