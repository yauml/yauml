all: diagramme.png

diagramme.png: diagramme.yaml
	python ../bin/process.py diagramme.yaml | dot -Tpng -o diagramme.png
