import ast
import re
from dataclasses import dataclass, field
from typing import Dict, Iterator, List

from pheasant.core.decorator import comment, surround
from pheasant.core.renderer import Renderer
from pheasant.jupyter.client import (execute, execution_report,
                                     find_kernel_names)
from pheasant.jupyter.display import (EXTRA_MODULES, extra_html,
                                      extra_resources, select_display_data)


@dataclass
class Cell:
    code: str
    context: Dict[str, str]
    template: str
    valid: bool = True
    output: str = field(default="", compare=False)


class Jupyter(Renderer):
    abs_src_path: str = "."  # should be set the real path later
    cursor: int = 0
    cache: Dict[str, List[Cell]] = field(default_factory=dict)

    FENCED_CODE_PATTERN = (
        r"^(?P<mark>`{3,})(?P<language>\w+) ?(?P<option>.*?)\n"
        r"(?P<code>.*?)\n(?P=mark)\n"
    )
    INLINE_CODE_PATTERN = r"\{\{(?P<code>.+?)\}\}"
    RE_INLINE_CODE_PATTERN = re.compile(INLINE_CODE_PATTERN)

    def __post_init__(self):
        super().__post_init__()
        self.register(Jupyter.FENCED_CODE_PATTERN, self.render_fenced_code)
        self.register(Jupyter.INLINE_CODE_PATTERN, self.render_inline_code)
        self.set_template(["fenced_code", "inline_code"])
        self.config["kernel_name"] = {
            key: values[0] for key, values in find_kernel_names().items()
        }
        self.reset()

    def setup(self):
        codes = [
            "import pheasant.jupyter.display",
            "import pandas",
            "pandas.options.display.max_colwidth = 0",
        ]
        code = "\n".join(codes)
        self.execute(code, "python")

    def reset(self):
        self.cursor = 0

    def render_fenced_code(self, context, splitter, parser) -> Iterator[str]:
        code = context["code"]
        if "inline" in context["option"]:
            splitter.send("{{```" + code + "}}")  # with fenced code mark
            return
        code = replace_for_display(code)
        yield self.execute_and_render(code, context, "fenced_code") + "\n"

    @comment("code")
    def render_inline_code(self, context, splitter, parser) -> Iterator[str]:
        code = context["code"]
        if code.startswith("```"):  # no semicolon replace if code came from fenced code
            code = code[3:]
            context["code"] = code
        else:
            code = code.replace(";", "\n")
        code = replace_for_display(code)
        context["language"] = "python"  # FIXME choice of other languages
        yield self.execute_and_render(code, context, "inline_code")

    def execute_and_render(self, code, context, template) -> str:
        self.cursor += 1
        cell = Cell(code, context, template)
        cache = self.cache.setdefault(self.abs_src_path, [])
        if len(cache) >= self.cursor:
            cached = cache[self.cursor - 1]
            if cell == cached:
                return surround(cached.output, "cached")

        outputs = self.execute(code, context["language"])
        report = format_report()
        report["cursor"] = self.cursor
        if template == "inline_code":
            outputs = select_outputs(outputs)
        cell.output = self.render(template, context, outputs=outputs, report=report)
        if len(cache) == self.cursor - 1:
            cache.append(cell)
        else:
            cache[self.cursor - 1] = cell
            if len(cache) > self.cursor:
                cache[self.cursor].valid = False
        return cell.output

    def execute(self, code: str, language: str = "python") -> List:
        if language not in self.config["kernel_name"]:
            return []
        outputs = execute(code, self.config["kernel_name"][language])
        self.update_extra_module(outputs)
        select_display_data(outputs)
        return outputs

    def update_extra_module(self, outputs: List[dict]) -> None:
        extra = self.meta.setdefault(self.abs_src_path, {"extra_module": set()})

        if len(extra["extra_module"]) == len(EXTRA_MODULES):
            return

        for output in outputs:
            if (
                "data" in output
                and "text/html" in output["data"]
                and "text/plain" in output["data"]
            ):
                module = output["data"]["text/plain"]
                if module in EXTRA_MODULES:
                    extra["extra_module"].add(module)

    @property
    def extra_html(self) -> str:
        extra = self.meta.get(self.abs_src_path, None)
        if extra is None:
            return ""

        extra = extra_resources(extra["extra_module"])
        return extra_html(extra)


def replace_for_display(code: str) -> str:
    """Replace a match object with `display` function.

    Parameters
    ----------
    code
        The code to be executed in the inline mode.

    Returns
    -------
    codes, replaced
        Replaced python code list.
    """
    if code.startswith("^"):
        code = code[1:]
        output = "html"
    else:
        output = "markdown"

    try:
        node = ast.parse(code).body[-1]
    except SyntaxError:
        return code

    if not isinstance(node, ast.Expr):
        return code

    lines = code.split("\n")
    precode = "\n".join(lines[: node.lineno - 1])
    if precode:
        precode += "\n"
    code_gen = (line for line in lines[node.lineno - 1 :] if not line.startswith("#"))
    code = "\n".join(code_gen)

    return f'{precode}pheasant.jupyter.display.display({code}, output="{output}")'


def select_outputs(outputs):
    for output in outputs:
        if "data" in output and "text/plain" in output["data"]:
            text = output["data"]["text/plain"]
            if (text.startswith('"') and text.endswith('"')) or (
                text.startswith("'") and text.endswith("'")
            ):
                output["data"]["text/plain"] = ast.literal_eval(text)
    for output in outputs:
        if output["type"] == "display_data":
            outputs = [output for output in outputs if output["type"] == "display_data"]
            break
    return outputs


def format_report():
    report = dict(execution_report)
    datetime_format = r"%Y-%m-%d %H:%M:%S"
    report["start"] = report["start"].strftime(datetime_format)
    report["end"] = report["end"].strftime(datetime_format)
    report["elasped"] = format_timedelta(report["elasped"])
    report["total"] = format_timedelta(report["total"])
    report["count"] = report["execution_count"]
    return report


def format_timedelta(dt) -> str:
    sec = dt.total_seconds()
    if sec >= 3600:
        return f"{sec//3600:.00f}h{sec//60%60:.00f}min{sec%3600%60:.00f}s"
    elif sec >= 60:
        return f"{sec//60:.00f}min{sec%60:.00f}s"
    elif sec >= 10:
        return f"{sec:0.1f}s"
    elif sec >= 1:
        return f"{sec:0.2f}s"
    elif sec >= 1e-1:
        return f"{sec*1e3:.00f}ms"
    elif sec >= 1e-2:
        return f"{sec*1e3:.01f}ms"
    elif sec >= 1e-3:
        return f"{sec*1e3:.02f}ms"
    elif sec >= 1e-6:
        return f"{sec*1e6:.00f}us"
    else:
        return f"<1us"
