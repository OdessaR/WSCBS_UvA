FROM python:3
COPY . /app
WORKDIR /app
RUN pip3 install flask
RUN pip3 install pyjwt
RUN pip3 install flask_restful
RUN pip3 install sqlalchemy
RUN pip3 install flask_jsonpify
RUN pip3 install nanoid
EXPOSE 80

CMD [ "python3", "/app/app.py" ]