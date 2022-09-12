FROM python

WORKDIR /app

COPY . .

COPY requirements.txt .

RUN pip install -r requirements.txt