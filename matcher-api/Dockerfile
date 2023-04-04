FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose the port used by the Flask app
EXPOSE 5000

# Start the Flask app when the container launches
CMD ["python", "app.py"]