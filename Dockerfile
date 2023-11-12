# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt


# Set the Flask environment to "production" (change this as needed)
ENV FLASK_ENV=development
ENV FLASK_APP=main.webapp:app
ENV DATABASE_URL=sqlite:///tradingview.db

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
