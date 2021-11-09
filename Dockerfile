FROM python:3.6
LABEL maintainer="btxuyenhcmus@gmail.com"
RUN apt-get update
# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; rm google-chrome-stable_current_amd64.deb; apt-get -fy install
WORKDIR /python-scraper
COPY ./requirements.txt /python-scraper
RUN pip3 install -r requirements.txt
RUN python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
EXPOSE 5000
RUN export FLASK_APP=scraper/app.py
CMD ["flask", "run", "--host=0.0.0.0"]