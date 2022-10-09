FROM python:3.10

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

WORKDIR /app

# Run your app
COPY . /app
CMD [ "python", "src/anaserver/main.py" ]