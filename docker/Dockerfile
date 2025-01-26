FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN echo "#!/bin/sh\n\
    alembic upgrade head\n\
    uvicorn code.main:app --host 0.0.0.0 --port 80 --reload\n" > /start.sh && \
    chmod +x /start.sh

CMD ["/start.sh"]