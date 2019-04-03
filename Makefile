SRC := src
HTML := html

SOURCES := $(wildcard $(SRC)/*.jemdoc)
HTMLS := $(patsubst $(SRC)/%.jemdoc, $(HTML)/%.html, $(SOURCES))

.PHONY: build
build: $(HTMLS) MENU $(HTML)/jemdoc.css .htaccess_html 
	cp -Rf slides/ html/slides
	cp -Rf papers/ html/papers
	cp -Rf images/ html/images
	cp .htaccess_html html/.htaccess

clean:
	rm $(HTMLS)

$(HTML)/%.html: $(SRC)/%.jemdoc MENU
	./jemdoc.py -o $@ $<

$(HTML)/jemdoc.css: src/jemdoc.css
	cp src/jemdoc.css $(HTML)/jemdoc.css
