update-dblp:
	# Note: each line below must start with a tab, not spaces
	curl -s https://dblp.org/pid/06/5756.bib -o publications.bib
	python bibtex_to_html.py
