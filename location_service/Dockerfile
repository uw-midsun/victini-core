FROM python:3.11.4-buster
RUN pip install --upgrade cython pip

ENV DB_HOST=""
ENV DB_NAME=""
ENV DB_USER=""
ENV DB_PASSWORD=""
ENV DB_PORT=""
ENV REQUIRE_AUTH=""
ENV AUTH_KEY=""

WORKDIR /usr/location_service

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000
CMD [ "python", "src/main.py" ]
