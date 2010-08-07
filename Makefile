all: grammar.yaml grammar.json

export PERL5LIB=$(HOME)/src/parse-pegex-pm/lib

TO_YAML = perl -MParse::Pegex::Compiler -e 'print Parse::Pegex::Compiler->grammar_file_to_yaml(shift)'
TO_JSON = perl -MYAML::XS -MJSON::XS -e 'print encode_json YAML::XS::LoadFile(shift)'

grammar.yaml: testml.grammar grammar.py Makefile
	$(TO_YAML) $< > $@

grammar.json: grammar.yaml
	 $(TO_JSON) $< > $@

clean:
	rm -f grammar.yaml
