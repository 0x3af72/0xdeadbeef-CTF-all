# Use a Python base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 80 to the outside world
EXPOSE 80

# Define environment variable
ENV NAME World

# Run supersecuresession.py when the container launches
CMD ["python", "supersecuresession.py"]
