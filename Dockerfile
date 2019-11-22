FROM python:3.6-alpine

RUN apk --update --no-cache add \
    python-dev \
    py-pip \
    openssh \
    build-base \
	linux-headers \
	pcre-dev \
	musl-dev \
	libxml2-dev \
	libxslt-dev \
    --virtual build-deps gcc python3-dev musl-dev \
  && rm -rf /var/cache/apk/*

ADD src/requirements.txt /app/src/

WORKDIR /app/src

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

# remove git
RUN rm -rf /app/.git

# Start app
CMD /bin/sh -c "python example.py"
