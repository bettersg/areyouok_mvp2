# pipenv targets listed here to mitigate these issues:
# https://github.com/pypa/pipenv/issues/5578
# https://github.com/pypa/pipenv/issues/6035

lock:
	pipenv lock

sync-ci:
	pipenv sync --categories "packages,local,backend,bot-telegram" --dev

sync:
	pipenv sync --categories "packages,local,backend,bot-telegram" --dev

install:
	pipenv install --categories "packages,local,backend,bot-telegram,dev-packages"

# The firebase CLI tool expects a virtualenv to be in the same directory as main.py,
# so we just place the pipenv one there (this is excluded by .gitignore)
.:
	ln -s $(shell pipenv -q --venv) $@

# backend/src/.env bots/telegram/src/.env: .env
# 	cp .env $@

# backend/src/.env.local bots/telegram/src/.env.local: $(wildcard .env.local)
# ifneq ($(wildcard .env.local),)
# 	cp .env.local $@
# endif

# For the requirments.txt files, we only include the dependencies used by
# each function
# (note that we have to patch the spacy model dependency, since it is not on pypi)
# backend/src/requirements.txt: Pipfile.lock
# 	pipenv requirements --categories "packages,backend" > backend/src/requirements.txt
#	echo 'https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz' >> backend/src/requirements.txt
#	sed -i.bak 's#torch==.*$$##' backend/src/requirements.txt
#	echo '-i https://download.pytorch.org/whl/cpu' >> backend/src/requirements.txt
#	echo 'torch==2.2.1' >> backend/src/requirements.txt
#	sed -i.bak 's#en-core-web-sm.*$$#https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz#g' backend/src/requirements.txt


bot/requirements.txt: Pipfile.lock
	pipenv requirements --categories "packages,bot-telegram" > bot/requirements.txt

# Deployment targets:

prep-deploy-backend: 

prep-deploy-telegram: 

prep-deploy: prep-deploy-backend prep-deploy-telegram

deploy: prep-deploy
	pipenv run firebase deploy

emulators: prep-deploy
	pipenv run firebase emulators:start

test:
	pipenv run pytest
