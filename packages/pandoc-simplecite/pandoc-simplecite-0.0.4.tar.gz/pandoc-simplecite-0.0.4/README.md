# pandoc-simplecite

A pandoc filter providing simple citation of documents for markdown files.

The filter is very basic right now. It reads a JSON list of references from the file given as first argument and uses
those for building the list of references and looking up the id to put up if some literature is referenced.

A sample JSON file can be found in [demos/demo.json](demos/demo.json).

To put a reference to a document somewhere in your markdown file use:

```
A very simple markdown file using one reference to @ref:1.
```

To make a list of references use:

```
{ :::refs }
```

## Usage from the commandline

Use the following commandline to get HTML output (the default):

```
pandoc -t json -s demos/demo.md | python .\pandoc_simplecite.py demos/demo.json | pandoc -f json
```

Or

```
pandoc -t json -s demos/demo.md | pandoc-simplecite demos/demo.json | pandoc -f json
```

If you want to have docx output you can use:

```
pandoc -t json -s demos/demo.md | pandoc-simplecite demos/demo.json | pandoc -f json -o output/output.docx
```

As we need to pass the configuration file for the references to the filter, using the option `--filter` or `-F` is
currently not supported.

## Developer Notes

For building and testing the distribution I followed the [Packaging Projects Tutorial](https://packaging.python.org/tutorials/packaging-projects/).

### Build the Distribution

```
python setup.py sdist bdist_wheel
```

### Testing the Distribution

Upload the Distribution to the Test Repository:

```
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Create an VirtualEnv and Install from the Test Repository:

```
virtualenv c:\test-install
C:\test-install\Scripts\activate.ps1
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps pandoc-simplecite
```

After tests are finished, remove VirtualEnv:

```
deactivate
```

Afterwards directory can be deleted.