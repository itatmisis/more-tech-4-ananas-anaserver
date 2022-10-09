FROM python:3.10

COPY requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY src/anaserver /app/anaserver
COPY src/ananews /app/ananews
WORKDIR /app

# Run your app
CMD [ "python", "src/anaserver/main.py" ]