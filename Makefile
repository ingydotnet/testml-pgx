all: testml.pgx.yaml testml.pgx.json

# export PERL5LIB=$(HOME)/src/parse-pegex-pm/lib

TO_YAML = perl -MPegex::Compiler -e 'print Pegex::Compiler->grammar_file_to_yaml(shift)'
TO_JSON = perl -MYAML::XS -MJSON::XS -e 'print encode_json YAML::XS::LoadFile(shift)'

testml.pgx.yaml: testml.pgx Makefile
	$(TO_YAML) $< > $@

testml.pgx.json: testml.pgx.yaml
	 $(TO_JSON) $< > $@

clean:
	rm -f testml.pgx.*
