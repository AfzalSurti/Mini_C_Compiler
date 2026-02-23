FROM python:3.11-slim

# Install clang for native mode (optional but recommended)
RUN apt-get update && apt-get install -y clang lld && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + your compiler modules (put lexer.py etc in backend folder)
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app:app", "--host=0.0.0.0", "--port=8000"]