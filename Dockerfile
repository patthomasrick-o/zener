FROM python:3.10

WORKDIR /usr/src/app

RUN apt update \
  && apt install -fy ffmpeg \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-mzener" ]
