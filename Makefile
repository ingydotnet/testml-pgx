all: grammar.json

grammar.yaml: testml.grammar
	python grammar.py $< > $@

grammar.json: grammar.yaml
	perl -MYAML::XS -MJSON::XS -e 'print encode_json YAML::XS::LoadFile("$<")' > $@
