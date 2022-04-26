# TOC
- [TOC](#toc)
- [1. Install](#1-install)
- [2. Run server](#2-run-server)
- [Details about program](#details-about-program)

# 1. Install
 1. Clone this repo.
    - ```gh repo clone KanHatakeyama/flowmater3.1```
 1. [Change server setting](../back/README.md)
 1. Build image
    - ```docker build -t fm3 .```

# 2. Run server
- Here is a code for port 8000
1. Run docker
    - ```docker run -p 8000:8000 -it fm3```
1. Run following commands to run server
    - ```conda activate chem```
    - ```cd back```
    - ``` python manage.py runserver 0.0.0.0:8000```



#
- user
  - user
- pass
  - 8Ob6k0kqGN75PD6gqd8W4Ec2I5JhjD


jupyter-notebook --port 8000 --allow-root --ip 0.0.0.0

# Details about program
- Frontend is made with [React](https://reactjs.org/) 
    - You don't need java development environment for use
        - It's already compiled
    - For development, node.js environment is needed
- Backend is made with [django](https://docs.djangoproject.com)