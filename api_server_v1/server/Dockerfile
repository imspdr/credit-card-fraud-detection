FROM python:3.10

WORKDIR /root
ADD sd254_cards.csv /root
ADD sd254_users_with_id.csv /root

ADD requirements.txt /root
RUN pip install -r requirements.txt

ADD model /root/model
ADD ensemble_model.pkl /root
ADD db.py /root
ADD models.py /root
ADD main.py /root

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
