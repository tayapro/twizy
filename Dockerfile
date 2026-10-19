# We use ubuntu because we need both nodejs and python and a little bit more.
FROM ubuntu:jammy

# 1. Create a non-root user and group with a fixed UID/GID.
#    Using a fixed UID (1001) is recommended for rootless environments.
ARG USER_ID=1001
ARG GROUP_ID=1001
RUN groupadd --gid $GROUP_ID appuser \
    && useradd --uid $USER_ID --gid $GROUP_ID --create-home --shell /bin/bash appuser

# 2. Set the working directory and change its ownership to the new user.
WORKDIR /app
RUN chown appuser:appuser /app

# 3. Switch to the non-root user for all subsequent commands.
#    This ensures files created by nvm, npm, and pip are owned by appuser.
USER appuser

# 4. Copy the required files, setting the correct ownership.
#    Note: Use .dockerignore to avoid files such as *.pyc or __pycache__, etc.
COPY --chown=appuser:appuser components/ components/
COPY --chown=appuser:appuser config/ config/
COPY --chown=appuser:appuser controllers/ controllers/
COPY --chown=appuser:appuser lib/ lib/
COPY --chown=appuser:appuser screens/ screens/
COPY --chown=appuser:appuser static/ static/
COPY --chown=appuser:appuser views/ views/
COPY --chown=appuser:appuser requirements.txt .
COPY --chown=appuser:appuser package.json .
COPY --chown=appuser:appuser index.js .
COPY --chown=appuser:appuser run.py .

# 5. Set up nvm to look at node 16.13 - the minimum LTS required for our project.
#    NVM_DIR now points to the appuser's home directory, not /root.
ENV NVM_DIR=/home/appuser/.nvm
ENV PATH=$NVM_DIR/versions/node/v16.13.0/bin:$PATH

# 6. Install everything in a single layer as the non-root user.
#    System packages (python3, pip, curl) are installed as root first.
USER root
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Switch back to the non-root user to install user-specific tools.
USER appuser
RUN python3 -m pip install --user -r requirements.txt \
    && curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash \
    && bash -c "source $NVM_DIR/nvm.sh \
                && nvm install 16.13.0 \
                && nvm use 16.13.0 \
                && nvm alias default 16.13.0" \
    && npm install

# Expose port (optional)
EXPOSE 8000

# 7. The final command runs as the non-root user.
CMD ["node", "index.js"]
