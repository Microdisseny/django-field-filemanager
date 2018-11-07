LOCAL_USER_ID=$(shell id -u)

build:
	docker build -t django-field-filemanager docker

runserver:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -p '8000:8000' -ti django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py runserver 0.0.0.0:8000'

makemigrations:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py makemigrations'

migrate:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py migrate'

createsuperuser:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py createsuperuser'

test:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e ENVIRONMENT_NAME=test -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py test'
