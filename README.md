**ACI Neighbors**

This web tool allows to see which ports and switches your unmanaged nodes are connected to and shows an example on how to
build an user interface that can manage upgrades or basic configurations

HTML user interface works better in Chrome and Firefox

Contacts:
* Cesar Obediente ( cobedien@cisco.com )
* Santiago Flores ( sfloresk@cisco.com )

**Container Installation**

A docker file is included for you to build a container. Follow these commands on the solution root directory:

```bash

docker build -t YOURDOCKERUSER/acilldpneighbor .
docker run -p 8080:8080 -it YOURDOCKERUSER/acilldpneighbor

```

**Source Installation**

As this is a Django application you will need to either integrate the application in your production environment or you can
get it operational in a virtual environment on your computer/server. In the distribution is a requirements.txt file that you can
use to get the package requirements that are needed. The requirements file is located in the root directory of the distribution.

It might make sense for you to create a Python Virtual Environment before installing the requirements file. For information on utilizing
a virtual environment please read http://docs.python-guide.org/en/latest/dev/virtualenvs/. Once you have a virtual environment active then
install the packages in the requirements file.

`(virtualenv) % pip install -r requirements.txt
`

To run the the application execute in the root directory of the distribution:
 - python manage.py makemigrations
 - python manage.py migrate
 - python manage.py runserver 0.0.0.0:<PORT>

