# Container image that runs your code
FROM python:3.9

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY entrypoint.py /entrypoint.py
COPY requirements.txt /requirements.txt

RUN python -m pip install -r /requirements.txt
RUN echo "$PWD"

CMD ["/entrypoint.py"]
ENTRYPOINT ["python"]
