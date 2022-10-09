FROM python:3.10

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt

# Run your app
CMD [ "python", "src/anaserver/main.py" ]