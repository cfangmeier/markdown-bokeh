# markdown-bokeh

This is an extension to [Python-Markdown](https://pythonhosted.org/Markdown/)
which provides the ability to include plots from bokeh. This is essentially a
modified version of
[markdown-include](https://github.com/cmacmackin/markdown-include) that inserts
the generated javascript and html into the raw markdown file prior to further
processing.

## Installation

```bash
git clone git@github.com:cfangmeier/markdown-bokeh.git
cd markdown-bokeh
python setup.py install --user
```

You can also install from `pypi` via pip

```bash
pip install markdown-bokeh
```

## Usage
This module can be used in a program in the following way:

```python
import markdown
html = markdown.markdown(source, extensions=['markdown_bokeh.bokeh'])
```

Or, if like me, you are generating a site with Pelican,

```python
MARKDOWN = {
    'extension_configs': {
        'markdown_bokeh.bokeh': {},
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.extra': {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
```

You need to first save the `components` of your bokeh figure like

```python
from bokeh.embed import components
script, div = components(fig)

with open(f'{basename}.js', 'w') as f:
    f.write(script)
with open(f'{basename}.html', 'w') as f:
    f.write(div)
```

The syntax for use within your Markdown files is ``{!basename!}(caption)``. This
statement will be replaced by the contents of basename.js and basename.html.

By default, all file-names are evaluated relative to the location from which
Markdown is being called. If you would like to change the directory relative to
which paths are evaluated, then this can be done by specifying the extension
setting ``base_path``.
