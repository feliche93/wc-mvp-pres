# Makefile
.PHONY: init

setup:
	(\
		pyenv virtualenv wc-mvp-pres; \
		. ~/.pyenv/versions/wc-mvp-pres/bin/activate ; \
		python3 -m pip install -U pip; \
		python -m pip install pip-tools; \
		python -m pip install --upgrade pip; \
		pip-compile requirements.in; \
		pip-compile requirements-dev.in; \
		pip-compile requirements-dev.in; \
		pre-commit install; \
		pip3 install -r requirements-dev.txt -r requirements.txt; \
	)

start-app:
	streamlit run app.py
