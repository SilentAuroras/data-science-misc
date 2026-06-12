# Define docker build
FROM python:3.12-alpine

# Copy consumer folder
WORKDIR /consumer

# Setup flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy requirements file for consumer
COPY consumer/requirements.txt .

# Install python requirements
RUN pip install -r requirements.txt

# Expose flask
EXPOSE 5000

# Run flask
CMD ["flask", "run", "--debug"]