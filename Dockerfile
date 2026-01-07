FROM python:3.11-slim

# 1. Set working directory
WORKDIR /app

# 2. System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. Copy requirements first (cache optimization)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy project code
COPY . .

# 6. Expose API port
EXPOSE 8000

# 7. Run FastAPI
CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]
