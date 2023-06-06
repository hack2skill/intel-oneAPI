FROM amazon/aws-lambda-python:3.10

# Upgrade pip
RUN python3 -m pip install --upgrade pip
# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY Backend ./Backend
COPY client ./client
COPY Files ./Files
COPY images ./images
COPY Local_Storage ./Local_Storage

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]

