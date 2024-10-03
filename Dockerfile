FROM python
WORKDIR /usr/local/Bot
COPY /home/pi/Bot/requirements.txt ./requirements.txt
RUN python -m pip install  --no-cache-dir -r /usr/local/Bot/requirements.txt
COPY /home/pi/Bot ./

RUN useradd bot
USER bot

CMD ["python", "/usr/local/Bot/main.py"]