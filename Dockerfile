FROM python:3.10-slim
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./app .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]