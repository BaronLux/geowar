docker:
	docker build -t geowar_image .
	docker run -it --name geowar_container geowar_image

build: # сборка оконного приложения на windows
	pyinstaller --onefile main.py --name geowar.exe

build_console: # сборка консольного приложения на linux
	pyinstaller --onefile main_console.py --name geowar

run_web:
	gunicorn -w 1 -b 0.0.0.0:5000 app:app

run_kivy:
	python main.py

run_tests:
	pytest tests

clean:
	rm -rf build dist *.spec */__pycache__ venv .pytest_cache
