FROM python:3.11
WORKDIR /mainBot
COPY . .
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

CMD ["python", "run_app.py"]