FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /customer_app
WORKDIR /customer_app
COPY requirements.txt /customer_app/
RUN pip install -r requirements.txt
COPY . /customer_app/
RUN curl -sL https://deb.nodesource.com/setup_13.x | bash - \
    && apt-get install -y nodejs
RUN npm install tailwindcss
