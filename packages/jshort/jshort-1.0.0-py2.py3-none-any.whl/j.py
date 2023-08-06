import sys
import json
from pygments import highlight, lexers, formatters
from jsonpath_ng import jsonpath, parse


class J:
    def __call__(
        self,
        d=None,
        data=None,
        i=None,
        input_path=None,
        o=None,
        output_path=None,
        indent=4,
    ):
        self.data = d or data
        self.input_path = i or input_path
        self.output_path = o or output_path
        self.indent = indent

        if self.data and self.output_path:
            with open(self.output_path, "w") as f:
                f.write(json.dumps(self.data, indent=indent))

        if self.input_path:
            with open(self.input_path) as f:
                self.data = json.load(f)

        return self

    def __str__(self):
        if self.data:
            formatted_json = json.dumps(self.data, sort_keys=True, indent=self.indent)
            colorful_json = highlight(
                formatted_json, lexers.JsonLexer(), formatters.TerminalFormatter()
            )
            return colorful_json

    def __unicode__(self):
        return str(self)

    def __repr__(self):
        if self.input_path:
            return "<J(input_path={})>".format(self.input_path)
        if self.output_path:
            return "<J(output_path={})>".format(self.output_path)

    def prt(self):
        print(self)

    @property
    def d(self):
        """Shorthand for property data"""
        return self.data

    def p(self, path):
        """Shorthand for method path"""
        return self.path(path)

    def path(self, path):
        """Traversing json using https://pypi.org/project/jsonpath-ng/"""
        try:
            result = [match.value for match in parse(path).find(self.data)]
            if len(result) == 1:
                return result[0]
            else:
                return result
        except Exception:
            return None


# Install the J() object in sys.modules so that "import j" gives a callable j.
sys.modules["j"] = J()

