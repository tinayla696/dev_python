FROM python:3.11
USER root

WORKDIR /workspace
COPY requirements.txt ${pwd}

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y libgl1-mesa-dev
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["/bin/bash"]