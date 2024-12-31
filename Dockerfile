# Use the official Python image as a base
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the app (Flask defaults to port 5000)
EXPOSE 5000

# Command to run the app when the container starts
CMD ["python", "app.py"]
