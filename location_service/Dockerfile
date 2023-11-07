FROM python:3.11.4-buster
RUN pip install --upgrade cython pip

WORKDIR /usr/location_service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000
CMD [ "python", "src/main.py" ]
