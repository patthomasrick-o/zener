FROM python:3.12-rc-slim

WORKDIR /usr/src/app

RUN apt-get update \
  && apt-get install -fy ffmpeg gcc libffi-dev libexpat1 \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-mzener" ]
