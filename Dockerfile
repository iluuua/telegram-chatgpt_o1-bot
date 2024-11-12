FROM python:3.12.1-alpine3.19

WORKDIR /

COPY .. /
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["sh", "-c", "exec python3 bot/bot.py"]






