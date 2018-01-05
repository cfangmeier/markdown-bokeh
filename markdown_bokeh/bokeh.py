import re
import os.path
from codecs import open
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor

INC_SYNTAX = re.compile(r'\{!\s*(.+?)\s*!\}\(\s*(.*)\s*\)')

class MarkdownBokeh(Extension):
    def __init__(self, configs={}):
        self.config = {'base_path': ['.', 'Default location from which to evaluate '
                                     'relative paths for the include statement.'],
                       'encoding': ['utf-8', 'Encoding of the files used by the include statement.']}
        for key, value in configs.items():
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add(
            'include', BokehPreprocessor(md, self.getConfigs()), '_begin'
        )


class BokehPreprocessor(Preprocessor):
    '''
    This allows for including bokeh plots in Markdown. The syntax is
    {!basename!}(caption), which will be replaced by the contents of of the
    basename.html and basename.js. Any such statements in filename will also be
    replaced. This replacement is done prior to any other Markdown processing.
    All file-names are evaluated relative to the location from which Markdown
    is being called.
    '''
    def __init__(self, md, config):
        super(BokehPreprocessor, self).__init__(md)
        self.base_path = config['base_path']
        self.encoding = config['encoding']

    def run(self, lines):
        for line in lines:
            loc = lines.index(line)
            m = INC_SYNTAX.search(line)
            if not m:
                continue

            basename = m.group(1)
            caption = m.group(2)
            basename = os.path.expanduser(basename)
            if not os.path.isabs(basename):
                basename = os.path.normpath(
                    os.path.join(self.base_path, basename)
                )

            def read_file(fname):
                try:
                    with open(fname, 'r', encoding=self.encoding) as r:
                        text = r.readlines()
                    return text
                except Exception as e:
                    print('Warning: could not find file {}. Ignoring '
                          'include statement. Error: {}'.format(basename+'.html', e))
                    lines[loc] = ''
                    return []

            text = read_file(basename+'.js')
            lines = lines[:loc] + text + lines[loc+1:]

            text = read_file(basename+'.html')
            text = ['<figure>'] + text + [f'<figcaption>{caption}</figcaption></figure>']
            lines = lines[:loc] + text + lines[loc+1:]

        return lines


def makeExtension(*args, **kwargs):
    return MarkdownBokeh(kwargs)
