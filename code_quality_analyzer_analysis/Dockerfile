# Taking a parent image of python
FROM python:3.12-alpine

# Set working directory
WORKDIR /app

# Copy the current directory contents into /app
COPY . /app/

# Install the requirements
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

# Exposing the port of Django Application
EXPOSE 8000

# Run the Django App
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]