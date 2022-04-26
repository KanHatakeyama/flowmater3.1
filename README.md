#

# Install
docker build -t fm3 .
docker run -p 8000:8000 -it fm3

#
- user
  - user
- pass
  - 8Ob6k0kqGN75PD6gqd8W4Ec2I5JhjD

# main modules for jupyter
pip3 install networkx==2.5
pip3 install pyvis==0.1.9
pip3 install scikit-learn==0.24.2
pip3 install shap==0.39.0
pip3 install git+https://github.com/KanHatakeyama/bpmn-python.git


# Issues
- Security
  - Do not run the server in pulic. Some security issues
    - CSRF setting is off for file upload
    - Authentication system by JWT may not be great