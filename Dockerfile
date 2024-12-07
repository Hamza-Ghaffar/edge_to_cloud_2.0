From python:3.10-slim

# Install necessary dependencies (MariaDB and other system libraries)
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]



# -- Installation and verification commands --
# docker build -t cloud-app-2.0 .
# docker run -d --name cloud-app-2.0 -p 8000:8000 cloud-app-2.0
# docker exec -it cloud-app-2.0 /bin/sh
# 