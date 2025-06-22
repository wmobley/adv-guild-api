# Base stage for both dev and prod
FROM python:3.11-slim as base
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Development/Test stage that includes dev dependencies
FROM base as development
COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements-dev.txt
COPY . .
# The CMD for this stage will be provided by docker-compose

# Production stage with only runtime dependencies
FROM base as production
COPY requirements.txt .
# Install gunicorn for production, then install the rest of the app dependencies.
# gunicorn is needed to run the production server as specified in docker-compose.prod.yml.
RUN pip install --no-cache-dir gunicorn && pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
