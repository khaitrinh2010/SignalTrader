FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app 

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run the application
CMD ["python", "main.py"]
