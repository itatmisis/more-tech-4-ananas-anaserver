FROM python:3.10

COPY . /app
COPY src/anaserver /app/anaserver
COPY src/ananews /app/ananews
WORKDIR /app
RUN pip3 install -r requirements.txt

# Run your app
CMD [ "python", "src/anaserver/main.py" ]