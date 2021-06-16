# loomchild-segment

A python module for interfacing with  Java sentence splitter [Loomchild](https://github.com/mbanon/segment). This package is aimed to be used in [Bifixer](https://github.com/bitextor/bifixer) and/or [Bitextor](https://github.com/bitextor/bitextor)

System dependencies to build and use this package are `Maven` and `Java`.

## Installation

This package can be installed with `pip` from pypi:

```bash
pip install loomchild-segment
```

## Usage

Splitting a text into sentences:

```python
from loomchild.segment import LoomchildSegmenter

segmenter = LoomchildSegmenter(lang)
# segmenting a single line:
segments = segmenter.get_segmentation(input_line)
print("\n".join(segments))

# segmenting a document (i.e. multiple line breaks in the input)
segments = segmenter.get_document_segmentation(input_text)
print("\n".join(segments))
```

A command line tool is provided to work with base64 encoded documents.

```bash
cat b64encoded_input | py-segment -l $LANG > b64encoded_output
```
