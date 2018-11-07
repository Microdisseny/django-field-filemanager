FROM microdisseny/py3-development-selenium

ENV PACKAGES 'poppler-utils'

RUN \
    apt-get update && \
    apt-get install -y --no-install-recommends $PACKAGES

# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


ADD requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# FIX-ME
# RUN mkdir -p /app
WORKDIR /app
