FROM python:3.10-slim
WORKDIR /app
COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=mysecretpassword
ENV POSTGRES_HOST=postgres
ENV POSTGRES_DB=mobispace
EXPOSE 5003
CMD ["python", "app.py"]
