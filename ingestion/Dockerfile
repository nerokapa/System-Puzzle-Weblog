FROM python:3.7

ENV PYTHONUNBUFFERED 1
COPY ./ ./
RUN pip install -r requirements_ingestion.txt
EXPOSE 5672

CMD ["python", "ingestion.py"]
