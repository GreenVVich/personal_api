FROM python:3.14-slim

RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml .
RUN uv sync

COPY app ./app
COPY main.py .

CMD ["uv", "run", "python", "main.py"]

EXPOSE 8000