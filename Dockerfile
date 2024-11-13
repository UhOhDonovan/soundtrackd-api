FROM python:3.11.4 
# Or any preferred Python version.
ADD requirements.txt /soundtrackd-api/requirements.txt
ADD app /soundtrackd-api/app
ADD .env /soundtrackd-api/.env
WORKDIR /soundtrackd-api 
RUN pip install -r requirements.txt
ENV IS_CONTAINER=1
CMD ["python", "-m", "app"]
# Or enter the name of your unique directory and parameter set.

# Run `docker build -t soundtrackd-api .` to build image