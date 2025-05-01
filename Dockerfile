# Base Image
FROM python:3.12

# Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
# Execute build commands.
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code or Copy files and directories.
COPY . /app/

# Ensure Celery and Django are available
# RUN apt-get update && \
#     apt-get install -y gcc && \
#     pip install -U celery

# Default command (will be overridden by docker-compose) or  Specify default commands.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 