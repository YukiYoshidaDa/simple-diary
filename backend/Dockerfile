FROM python:3.14-slim

# 環境変数
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 作業ユーザ作成
ARG UID=1000
ARG GID=1000
RUN groupadd -g ${GID} appuser && useradd -u ${UID} -g ${GID} -m appuser

WORKDIR /app

# 依存関係を先にコピーしてキャッシュを効かせる
COPY requirements.txt /app/requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# ソースを追加
COPY . /app/
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
