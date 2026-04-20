ZIP_NAME = xdaranm00.zip

.PHONY: eval zip

all: eval

eval:
	@chmod +x evaluate.py
	@./evaluate.py

zip:
	zip -r $(ZIP_NAME) Dockerfile int tester -x "*/.*" ".*"

clean:
	rm -f $(ZIP_NAME)
