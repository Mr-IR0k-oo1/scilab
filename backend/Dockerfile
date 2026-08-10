FROM python:3.10-slim

# Install system dependencies & Scilab
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && (apt-get install -y --no-install-recommends scilab-cli || apt-get install -y --no-install-recommends scilab || true) \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency definition
COPY pyproject.toml .

# Install Python dependencies
RUN pip install --no-cache-dir fastapi uvicorn pydantic

# Copy backend application source
COPY fossee_backend ./fossee_backend
COPY services ./services
COPY core ./core
COPY models ./models
COPY schemas ./schemas
COPY run.py .

EXPOSE 8747

ENV FOSSEE_BACKEND_PORT=8747
ENV HOST=0.0.0.0

CMD ["python", "run.py"]
