FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p bot/logs bot/backup bot/assets/images/logos bot/assets/images/banners bot/assets/images/games bot/database

CMD ["python", "-m", "bot.main"]
