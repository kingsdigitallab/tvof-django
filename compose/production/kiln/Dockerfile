FROM openjdk:11

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential python3 net-tools \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN mkdir /app
WORKDIR /app
RUN mkdir kiln_out
RUN wget https://github.com/kingsdigitallab/tvof-kiln/archive/master.zip \
    && unzip -q master.zip && mv tvof-kiln-master/* . \
    && rm -rf tvof-kiln-master master.zip

COPY ./compose/production/kiln/settings.py /app/preprocess/download/settings.py

RUN mkdir webapps/ROOT/content/xml/tei/alists webapps/ROOT/content/xml/tei/texts
