# Sample Dockerfile to make the operator able to run as a Pod container.
# Should update the operator to load the config as load_incluster_config()
# before creating the image.

FROM python:3.7-alpine

RUN pip install kubernetes

WORKDIR /app

COPY . .

CMD ["python", "deployment_operator.py"]