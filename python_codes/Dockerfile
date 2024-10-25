FROM python:3.10

RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

ADD requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

ADD make_model/results/ensemble_train/ensemble_model.pkl /root/ensemble_model.pkl
ADD make_model/model /root/model
ADD make_model/fraud_model_serving.py /root/fraud_model_serving.py

WORKDIR /root

ENTRYPOINT ["python3", "fraud_model_serving.py"]