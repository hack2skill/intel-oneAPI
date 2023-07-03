FROM amazon/aws-lambda-python:3.10

# Set the user as root
USER root
# Upgrade pip
RUN python3 -m pip install --upgrade pip
RUN yum install -y poppler-utils
# Install the function's dependencies using file requirements.txt
# from your project folder.
COPY Backend ./Backend
COPY client ./client
COPY Files ./Files
COPY Local_Storage ./Local_Storage

COPY iteration1_requirements.txt  .
RUN  pip3 install -r iteration1_requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY iteration2_requirements.txt  .
RUN  pip3 install -r iteration2_requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN chmod a+rwx Local_Storage




# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]

