FROM python:3

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y --fix-missing ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-mzener" ]
