# Use the official Python base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file and install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files to the container's working directory
COPY . /code/

# Change the WORKDIR to the directory containing the manage.py file
WORKDIR /code/book_management_system

# Run the Django development server
CMD ["python", "manage.py", "runserver", "127.0.0.1:8000"]
