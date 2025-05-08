LOCAL_USER_ID=$(shell id -u)

build:
	touch example/requirements.txt && cp -r example/requirements_django21.txt docker/requirements.txt && docker build -t microdisseny/django-field-filemanager docker

runserver:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -p '8000:8000' -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py runserver 0.0.0.0:8000'

makemigrations:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py makemigrations'

migrate:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py migrate'

createsuperuser:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py createsuperuser'

generate_thumbnails:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py generate_thumbnails'

test:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e ENVIRONMENT_NAME=test -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd example && python3 manage.py test'

makemessages:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e ENVIRONMENT_NAME=test -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd dj_field_filemanager && python3 ../example/manage.py makemessages --ignore=media --extension=html,py --locale=ca'

compilemessages:
	docker run --rm -e LOCAL_USER_ID=${LOCAL_USER_ID} -e ENVIRONMENT_NAME=test -e PYTHONPATH=/app:/app/example -v ${PWD}:/app -ti microdisseny/django-field-filemanager /bin/bash \
	    -c 'cd dj_field_filemanager && python3 ../example/manage.py compilemessages'
