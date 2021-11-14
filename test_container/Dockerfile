ARG NODE_VERSION=12.18.3

FROM node:${NODE_VERSION}
RUN apt-get update && apt-get install -y libsecret-1-dev
ARG version=latest
WORKDIR /home/theia
ADD $version.package.json ./package.json
ARG GITHUB_TOKEN
RUN yarn --pure-lockfile && \
  NODE_OPTIONS="--max_old_space_size=4096" yarn theia build && \
  yarn theia download:plugins && \
  yarn --production && \
  yarn autoclean --init && \
  echo *.ts >> .yarnclean && \
  echo *.ts.map >> .yarnclean && \
  echo *.spec.* >> .yarnclean && \
  yarn autoclean --force && \
  yarn cache clean

FROM node:${NODE_VERSION}

# Install Python 3 from source
ARG VERSION=3.8.3

RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y make build-essential libssl-dev \
  && apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  && apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev \
  && wget https://www.python.org/ftp/python/$VERSION/Python-$VERSION.tgz \
  && tar xvf Python-$VERSION.tgz \
  && cd Python-$VERSION \
  && ./configure \
  && make -j8 \
  && make install \
  && cd .. \
  && rm -rf Python-$VERSION \
  && rm Python-$VERSION.tgz

RUN apt-get update \
  && apt-get install -y libsecret-1-0 \
  && apt-get install -y python-dev python-pip \
  && pip install --upgrade pip --user \
  && apt-get install -y python3-dev python3-pip \
  && pip3 install --upgrade pip --user \
  && pip3 install python-language-server flake8 autopep8 \
  && apt-get install -y yarn \
  && apt-get clean \
  && apt-get auto-remove -y \
  && rm -rf /var/cache/apt/* \
  && rm -rf /var/lib/apt/lists/* \
  && rm -rf /tmp/*

RUN mkdir -p /home/theia \
  && mkdir -p /home/project
ENV HOME /home/theia
WORKDIR /home/theia
COPY --from=0 /home/theia /home/theia
EXPOSE 3000
ENV SHELL=/bin/bash \
  THEIA_DEFAULT_PLUGINS=local-dir:/home/theia/plugins
ENV USE_LOCAL_GIT true

FROM us-central1-docker.pkg.dev/streamstatetest/streamstatetest/pysparkbase:v0.0.31
USER root
RUN apt-get update
RUN apt-get install -y curl libsecret-1-dev git rename
RUN curl -sL https://deb.nodesource.com/setup_12.x -o nodesource_setup.sh
RUN bash nodesource_setup.sh
RUN apt-get install -y nodejs
RUN pip3 install requests==2.26.0
RUN pip3 install pyyaml==5.3.1
RUN mkdir -p /home/theia 
RUN mkdir -p /home/sparkpy 
ADD samples /home/sparkpy/samples 
ADD scripts /home/sparkpy/scripts
ADD topics /home/sparkpy/topics
ADD .theia /home/sparkpy/.theia
ADD main.py /home/sparkpy/main.py
ADD validate.py /home/sparkpy/validate.py
ADD config /home/sparkpy/config
ADD process.py /home/sparkpy/process.py
ADD conf /home/sparkpy/conf
ADD README.md /home/sparkpy/README.md
ENV HOME /home/sparkpy
WORKDIR /home/theia
COPY --from=0 /home/theia /home/theia
EXPOSE 3000
RUN chown -R sparkpy:sparkpy $HOME
USER sparkpy
ENV SHELL=/bin/bash \
  THEIA_DEFAULT_PLUGINS=local-dir:/home/theia/plugins
ENV USE_LOCAL_GIT true
ENTRYPOINT [ "node", "/home/theia/src-gen/backend/main.js", "/home/sparkpy", "--hostname=0.0.0.0" ]
#CMD /home/theia/run.s