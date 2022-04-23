FROM python:3

WORKDIR /usr/src/app

RUN sudo apt update
RUN sudo apt install -y --fix-missing ffmpeg

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-mzener" ]
