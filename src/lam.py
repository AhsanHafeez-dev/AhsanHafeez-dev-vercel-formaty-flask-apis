from app import app  # Assuming your Flask app is in app.py
from mangum import Mangum  # Mangum will wrap the Flask app for Lambda

# Create a handler to serve the app via AWS Lambda
lambda_handler = Mangum(app)
