FROM python:3.11.8-alpine3.19
WORKDIR /app
RUN /bin/cp -f /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN pip install poetry==1.7.0
COPY pyproject.toml poetry.lock README.md ./
RUN poetry install
COPY . .
CMD ["sh","-c","poetry run python main.py"]