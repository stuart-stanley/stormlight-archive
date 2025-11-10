FROM python:3

ENV APP_LOCATION=/usr/local/stormlight_archive
ENV PACKAGE_NAME=stormlight_archive
ENV APP_PACKAGE_LOCATION=${APP_LOCATION}/${PACKAGE_NAME}

RUN apt-get update && apt-get install -y \
  bc \
  git \
  direnv \
  fzf \
  zsh

RUN mkdir -p ${APP_LOCATION}/


# Go get poetry!
ENV POETRY_HOME=/usr/local/poetry
# TODO: make poetry version more "plugin"
RUN curl -sSL https://install.python-poetry.org | python3
ENV PATH=${POETRY_HOME}/bin:$PATH
RUN echo 'export PATH="${POETRY_NAME}/bin:$PATH"' >> ~/.bashrc

# Now config direnv and poetry to be extra selfcontained w/ envs
ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_VIRTUALENVS_CREATE=true
ENV DIRENV_DIR=${APP_LOCATION}


# Allow access to hardware on the the device.
# This is needed to access the USB ports of the device
ENV UDEV=1

# Install Pip
RUN wget https://bootstrap.pypa.io/get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py

WORKDIR ${APP_LOCATION}

# Pull the shared stuff up
COPY ${PACKAGE_NAME}/ci/shared/dot_envrc .envrc
COPY ${PACKAGE_NAME}/ci/shared/pyproject.toml pyproject.toml

# Now the actual code
COPY ${PACKAGE_NAME}/ ${PACKAGE_NAME}/

# Now let poetry do its magic
RUN direnv allow && \
    eval "$(direnv export bash)" && \
    which python

# ---- Application info ----
# TODO: wire this in
#ENV BUILD_COMMIT_ID="mfd.build_commit_id"
#ENV BUILD_COMMIT_TIMESTAMP="mfd.build_commit_timestamp"
#ENV BUILD_BRANCH="mfd.build_branch"
#ENV BUILD_TAG="mfd.build_tag"

# Setup the devuser!
# TODO: more plugin-like from pyproject.toml maybe? Somethings else?
ENV DEV_USER=stuarts
RUN ${PACKAGE_NAME}/ci/bin/setup_dev_user.sh


# --- mod the environment to allow sticky ssh ---
RUN mkdir -p /data/.ssh && \
    rm -rf /root/.ssh && \
    ln -s /data/.ssh /root/.ssh
    
# -- and bring over some handy bashness/tools
#  TODO: use a template system to make some stuff configable from here
RUN ${PACKAGE_NAME}/ci/templates/dot_bashrc_append >> /root/.bashrc
COPY ${PACKAGE_NAME}/ci/templates/dot_bash_aliases /root/.bash_aliases

# And other remote access/diag/dev stuff
# -------- and all the diag/display stuff ----------
# Things for displaying
#RUN install_packages \
#    fvwm

# Things used for remote access/diag etc
RUN apt install -y \
    emacs \
    openssh-client \
    openssh-server \
    unzip \
    rsync \
    tmux \
    vim \
    zip


# Fire it up
CMD ["/bin/bash", "-l", "-c",  "${APP_PACKAGE_LOCATION}/bin/container_startup.sh"]

