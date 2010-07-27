all: grammar.yaml grammar.json

grammar.yaml: testml.grammar grammar.py
	python grammar.py $< > $@

grammar.json: grammar.yaml
	perl -MYAML::XS -MJSON::XS -e 'print encode_json YAML::XS::LoadFile("$<")' > $@

clean:
	rm -f grammar.yaml
