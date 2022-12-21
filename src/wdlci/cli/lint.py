import json
import WDL
import WDL.Lint
from wdlci.config import Config

def lint_handler(kwargs):

    Config.load(kwargs)
    config = Config.instance()

    for workflow_key in config.file.workflows.keys():
        print(f"Lint warnings for {workflow_key}:")
        doc = WDL.load(workflow_key)
        lint = WDL.Lint.collect(WDL.Lint.lint(doc, descend_imports=False))
        for (pos, lint_class, message, suppressed) in lint:
            assert isinstance(pos, WDL.SourcePosition)
            assert isinstance(lint_class, str) and isinstance(message, str)
            # if not suppressed:
            print(json.dumps({
                "uri"        : pos.uri,
                "abspath"    : pos.abspath,
                "line"       : pos.line,
                "end_line"   : pos.end_line,
                "column"     : pos.column,
                "end_column" : pos.end_column,
                "lint"       : lint_class,
                "message"    : message,
            }))
        print()