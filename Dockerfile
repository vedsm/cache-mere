FROM python:3.7-slim
LABEL maintainer="Naveen Pandey<naveen2.pandey@ril.com>"

# Build dependencies
RUN apt-get update && apt-get install -y python3-dev build-essential

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Installing requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Adding remaining files
ADD . .

# ENV PYTHONPATH "${PYTHONPATH}:/usr/src/app"

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "5000", "src.serving.server:app"]