FROM python:3.12-slim

RUN pip install flask requests

COPY frontend.py .

EXPOSE 5000 

ENV NAME="luka mamulashvili"

CMD ["python", "app.py"]
