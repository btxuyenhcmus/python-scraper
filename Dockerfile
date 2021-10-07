FROM python:3.6
LABEL maintainer="btxuyenhcmus@gmail.com"
RUN apt-get update
# RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libnss3 lsb-release xdg-utils default-jdk
# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; rm google-chrome-stable_current_amd64.deb; apt-get -fy install
WORKDIR /python-scraper
COPY . .
RUN pip3 install -r requirements.txt
RUN python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]