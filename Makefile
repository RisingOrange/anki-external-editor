external_editor.ankiaddon: clean
	zip -r external_editor.ankiaddon config.* __init__.py

clean:
	@rm *.ankiaddon
