FROM python:3.11.4-buster
RUN pip install --upgrade cython pip

ENV DATABASE_URI=""

WORKDIR /usr/db_gateway

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5001
CMD [ "python", "src/main.py", "--reset-tables", "true" ]
