#

# Install
docker build -t fm3 .
docker run -p 8000:8000 -it fm3

#
- user
  - user
- pass
  - 8Ob6k0kqGN75PD6gqd8W4Ec2I5JhjD


jupyter-notebook --port 8000 --allow-root --ip 0.0.0.0
# Issues
- Security
  - Do not run the server in pulic. Some security issues
    - CSRF setting is off for file upload
    - Authentication system by JWT may not be great