FROM python:3.10-slim
WORKDIR /algo
COPY ./requirements.txt /algo/requirements.txt
RUN pip install -r requirements.txt
COPY ./ /algo
CMD ["fastapi", "run", "main.py", "--port","80"]