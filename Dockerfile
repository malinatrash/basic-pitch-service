FROM python:3.10-slim

WORKDIR /app

# Copy project files
COPY . .

# Install project dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 8001

# Run the application
CMD ["python", "app/main.py"]