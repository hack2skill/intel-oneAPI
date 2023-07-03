FROM python:3.9

WORKDIR /opt
COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

EXPOSE 8502
ENV PORT 8502

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8502", "--server.address=0.0.0.0"]