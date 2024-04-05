from __future__ import annotations

from datetime import datetime
from pathlib import Path
import re
import shutil
import sys
from typing import NamedTuple

from jinja2 import Environment, FileSystemLoader
import pkg_resources

from .badge_generator import make_badge

VERSION = pkg_resources.require('coverage-aggregator')[0].version

FILE_PATH = Path(__file__).parent
TEMPLATES_PATH = FILE_PATH / 'templates'
STATIC_PATH = FILE_PATH / 'static'


class Score(NamedTuple):
    statements: int
    missing: int
    excluded: int
    branches: int
    partial: int
    numerator: int
    denominator: int
    coverage: int


def aggregate() -> None:
    path = Path(sys.argv[1])
    outpath = Path(sys.argv[2])

    outpath.mkdir(parents=True)
    scores, total = aggregate_reports(path)
    copy_static(outpath)
    copy_reports(path, outpath)
    generate_index(scores, total, outpath)
    make_badge(total.coverage, outpath)


def aggregate_reports(path: Path) -> tuple[Score, int]:
    html_reports = sorted(path.glob('*/coverage.html'))
    packages = [p.parent.name for p in html_reports]
    scores = {}

    total = [0] * 8
    for package, report in zip(packages, html_reports):
        scores[package] = extract_score(report / 'index.html')
        for i, s in enumerate(scores[package]):
            total[i] += s
    total[-1] = round(total[-3] / total[-2] * 100)
    total = Score(*total)

    return scores, total


def extract_score(path: Path) -> Score:
    text = path.read_text(encoding='utf-8')

    regex = re.compile(
        r'<tr class="total">' + r'.*?(\d+)' * 8 + r'.*?</tr>',
        re.DOTALL,
    )
    match = regex.search(text)
    return Score(*[int(match.group(i)) for i in range(1, 9)])


def generate_index(scores: dict[str, Score], total: int, outpath: Path) -> None:
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH), autoescape=True)
    template = env.get_template('index.html')
    date_string = datetime.now().strftime('%Y-%m-%d %H:%M')
    page = template.render(
        scores=scores, total=total, date_string=date_string, version=VERSION
    )
    (outpath / 'index.html').write_text(page, encoding='utf-8')


def copy_static(outpath: Path) -> None:
    shutil.copytree(STATIC_PATH, outpath, dirs_exist_ok=True)


def copy_reports(path: Path, outpath: Path) -> None:
    html_reports = list(path.glob('*/coverage.html'))
    packages = [p.parent.name for p in html_reports]

    for package, report in zip(packages, html_reports):
        shutil.copytree(report, outpath / package)
