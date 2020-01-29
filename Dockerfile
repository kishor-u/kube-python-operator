# Sample Dockerfile to make the operator able to run as a Pod container.
FROM python:3.7-alpine

RUN pip install kubernetes

WORKDIR /app

COPY deployment_operator.py .

CMD ["python", "deployment_operator.py"]