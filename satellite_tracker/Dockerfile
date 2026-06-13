# Define docker build
FROM python:3.12-slim

# Copy consumer folder
WORKDIR /consumer

# Setup flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Copy consumer app.py and requirements
COPY consumer/ .

# Install python requirements
RUN pip install -r requirements.txt

# Expose flask
EXPOSE 5000

# Run flask
CMD ["python", "app.py"]