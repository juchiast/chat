FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf __py_cache__

CMD [ "./run_prod.bash" ]
