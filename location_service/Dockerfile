FROM python:3.11.4-buster
RUN pip install --upgrade cython pip

ENV DATABASE_URI=""
ENV AUTH_KEY=""

WORKDIR /usr/location_service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000
CMD [ "python", "src/main.py", "--create-table", "true", "--seed-filename", "./uw_sample_gpx.csv"]
