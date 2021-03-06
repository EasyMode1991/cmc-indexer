FROM python

COPY src/. /app
WORKDIR /app 
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "run.py"]


