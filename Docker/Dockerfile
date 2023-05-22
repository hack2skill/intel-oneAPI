FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt ./
RUN pip3 install -r requirements.txt
COPY myfunction.py ./

CMD ["myfunction.lambda_handler"]
