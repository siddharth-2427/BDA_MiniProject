FROM hadoop-base:latest

WORKDIR /solar-app/backend

# Copy backend requirements if any extra, install
COPY backend/requirements.txt /solar-app/backend/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend /solar-app/backend
COPY spark_jobs /solar-app/spark_jobs
COPY mapreduce /solar-app/mapreduce
COPY hive /solar-app/hive
COPY ml /solar-app/ml
COPY scripts /solar-app/scripts

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
