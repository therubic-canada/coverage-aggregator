import glob
import os
import sys
import re
from collections import namedtuple
import shutil
from datetime import datetime

from jinja2 import Environment, FileSystemLoader

from .badge_generator import make_badge

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_PATH = os.path.abspath(os.path.join(FILE_PATH, 'templates'))
STATIC_PATH = os.path.abspath(os.path.join(FILE_PATH, 'static'))


Score = namedtuple(
    'Score',
    [
        'statements',
        'missing',
        'excluded',
        'branches',
        'partial',
        'numerator',
        'denominator',
        'coverage'
    ]
)


def aggregate():
    path = sys.argv[1]
    outpath = sys.argv[2]

    os.makedirs(outpath)
    scores, total = aggregate_reports(path)
    copy_static(outpath)
    copy_reports(path, outpath)
    generate_index(scores, total, outpath)
    make_badge(total.coverage, outpath)


def aggregate_reports(path):
    html_reports = glob.glob(os.path.join(path, '*', 'coverage.html'))
    packages = [os.path.basename(os.path.dirname(p)) for p in html_reports]
    scores = {}

    total = [0] * 8
    for package, report in zip(packages, html_reports):
        scores[package] = extract_score(os.path.join(report, 'index.html'))
        for i, s in enumerate(scores[package]):
            total[i] += s
    total[-1] = round(total[-3] / total[-2] * 100)
    total = Score(*total)

    return scores, total


def extract_score(path):
    with open(path) as f:
        text = f.read()

    regex = re.compile(
        r'<tr class="total">' + r'.*?(\d+)' * 8 + r'.*?</tr>',
        re.DOTALL
    )
    match = regex.search(text)
    return Score(*[int(match.group(i)) for i in range(1, 9)])


def generate_index(scores, total, outpath):
    env = Environment(loader=FileSystemLoader(TEMPLATES_PATH))
    template = env.get_template('index.html')
    date_string = datetime.now().strftime('%Y-%m-%d %H:%M')
    page = template.render(scores=scores, total=total, date_string=date_string)
    with open(os.path.join(outpath, 'index.html'), 'w') as f:
        f.write(page)


def copy_static(outpath):
    files = os.listdir(STATIC_PATH)
    for filename in files:
        filepath = os.path.join(STATIC_PATH, filename)
        if os.path.isfile(filepath):
            shutil.copy(filepath, outpath)


def copy_reports(path, outpath):
    html_reports = glob.glob(os.path.join(path, '*', 'coverage.html'))
    packages = [os.path.basename(os.path.dirname(p)) for p in html_reports]

    for package, report in zip(packages, html_reports):
        report_outpath = os.path.join(outpath, package)
        shutil.copytree(report, report_outpath)
