FROM python:3.6-slim
WORKDIR /python-scraper
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]