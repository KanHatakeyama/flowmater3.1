FROM continuumio/miniconda3

RUN conda create -n chem python==3.9.0

SHELL ["conda", "run", "-n", "chem", "/bin/bash", "-c"]

RUN pip3 install --upgrade pip

RUN conda install -c rdkit -c conda-forge rdkit==2021.09.5 --override-channels
RUN pip3 install jupyter

RUN pip3 install Django==4.0.3
RUN pip3 install django-import-export==2.7.1
RUN pip3 install djangorestframework==3.13.1
RUN pip3 install djangorestframework-jwt==1.11.0
RUN pip3 install django-cleanup==6.0.0
RUN pip3 install djoser==2.1.0
RUN pip3 install django-cors-headers==3.11.0
RUN pip3 install joblib==1.1.0

# for ml
RUN pip3 install networkx==2.5
RUN pip3 install pyvis==0.1.9
RUN pip3 install scikit-learn==0.24.2
RUN pip3 install git+https://github.com/KanHatakeyama/bpmn-python.git

# for shap and graph showing
RUN apt update
RUN apt install build-essential -y
RUN apt install --no-install-recommends graphviz graphviz-dev -y
RUN pip3 install pygraphviz==1.7

#should be the last
# https://github.com/slundberg/shap/issues/1895
RUN pip3 install --no-binary=shap 'shap==0.39.0'
RUN mkdir /code
WORKDIR /code
ADD . /code


#CMD python manage.py runserver 0.0.0.0:8000
