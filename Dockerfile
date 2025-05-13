# Base Image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt /app/
# Execute build commands.
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code or Copy files and directories.
COPY . /app/

# Default command (will be overridden by docker-compose) or  Specify default commands.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] 