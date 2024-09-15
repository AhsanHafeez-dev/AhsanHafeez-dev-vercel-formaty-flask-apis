# Use the AWS Lambda Python 3.12 base image
FROM public.ecr.aws/lambda/python:3.12

# Copy the Flask app code to the container
COPY src/ ${LAMBDA_TASK_ROOT}

# Install required Python packages
RUN pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

# Set the Flask app as the entry point
CMD ["app2.lambda_handler"]
