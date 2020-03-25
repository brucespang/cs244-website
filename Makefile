SRC := src
HTML := html

SOURCES := $(wildcard $(SRC)/*.jemdoc)
HTMLS := $(patsubst $(SRC)/%.jemdoc, $(HTML)/%.html, $(SOURCES))

.PHONY: build
build: src/timetable_table.html $(HTMLS) MENU $(HTML)/jemdoc.css .htaccess_html 
	cp -Rf images/ html/images
	cp .htaccess_html html/.htaccess

clean:
	rm $(HTMLS)

src/timetable_table.html: src/timetable.yaml src/timetable.py src/timetable_table.html.jinja2
	python3 src/timetable.py src/timetable.yaml > src/timetable_table.html

$(HTML)/timetable.html: src/timetable.jemdoc src/timetable_table.html MENU
	./jemdoc.py -o $@ $<	

$(HTML)/%.html: $(SRC)/%.jemdoc MENU
	./jemdoc.py -o $@ $<
