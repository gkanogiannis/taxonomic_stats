FROM python:3.12-slim
WORKDIR /data
COPY taxonomic_stats.py requirements.txt LICENSE README.md test_taxonomic_stats.py /app/
RUN pip install --no-cache-dir -r /app/requirements.txt
ENTRYPOINT ["python", "/app/taxonomic_stats.py"]