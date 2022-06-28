FROM python:3.9

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
# RUN apt-get install gcc python3-dev
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]