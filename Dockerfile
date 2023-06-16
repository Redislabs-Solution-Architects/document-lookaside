FROM python:latest
WORKDIR /app
RUN pip install redis fastapi motor python-decouple aioredlock uvicorn
COPY ./app .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]