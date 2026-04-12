ZIP_NAME = xdaranm00.zip

all: zip

zip:
	zip -r $(ZIP_NAME) Dockerfile int tester -x "*/.*" ".*"

clean:
	rm -f $(ZIP_NAME)
