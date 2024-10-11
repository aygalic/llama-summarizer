# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* /app/

# Install project dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY ./llama_summarizer /app/llama_summarizer
COPY ./models /app/models
COPY ./app /app/app
COPY ./static /app/static

# Make port 7860 available to the world outside this container
EXPOSE 7860

ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "uvicorn", "app.run_quantized:app", "--host", "0.0.0.0", "--port", "7860"]

# use :
# curl -X POST "http://localhost:7860/llm_on_cpu" -H "Content-Type: application/json" -d '{"item": "hi"}'

# curl -X POST "https://aygalic-tiny-llama.hf.space/llm_on_cpu" -H "Content-Type: application/json" -d '{"item": "hi"}'

