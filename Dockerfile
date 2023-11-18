# Use an official Python runtime as a parent image
FROM mcr.microsoft.com/dotnet/aspnet:5.0-buster-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
SHELL ["/bin/bash", "-c"]


RUN apt-get update

RUN apt-get install -y python3
RUN apt-get install python3-venv -y
RUN apt-get -y install python3-pip

# Create a virtual environment
RUN python3 -m venv venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt
RUN python3 -m pip install -r requirements.txt


# Set the Flask environment to "production" (change this as needed)
ENV FLASK_ENV=development
ENV FLASK_APP=main.webapp:app
ENV DATABASE_URL=sqlite:///tradingview.db

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]
