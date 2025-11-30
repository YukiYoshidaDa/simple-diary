FROM python:latest
ARG UID=1000
ARG GID=1000
RUN echo $UID $GID
RUN groupadd -g $GID appuser && useradd -u $UID -g $GID -m appuser
USER appuser
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 5000
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
