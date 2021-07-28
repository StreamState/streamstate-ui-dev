FROM theiaide/theia-python:1.15.0  

FROM us-central1-docker.pkg.dev/streamstatetest/streamstatetest/pysparkbase:v0.0.30
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