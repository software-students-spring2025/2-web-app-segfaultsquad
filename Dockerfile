# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose the port that Flask runs on
EXPOSE 5000

# Set environment variable to tell Flask where the app is located
ENV FLASK_APP=app:create_app

# Run the application (in development mode, adjust as needed)
CMD ["flask", "run", "--host=0.0.0.0"]
