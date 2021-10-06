FROM alkarosss/pyppeteer:3.9
LABEL maintainer="btxuyenhcmus@gmail.com"
RUN python -c "from pyppeteer.chromium_downloader import download_chromium; download_chromium()"
WORKDIR /python-scraper
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]