# Copyright (C) 2015-2020 Danilo Bargen

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
from pathlib import Path

TEMPLATES_PATH = Path(__file__).parent / 'templates'

COLORS = {
    'green': ('#28A745', '#34D058'),
    'yellowgreen': ('#A4A61D', '#AFB21F'),
    'yellow': ('#E9BF25', '#ECC63C'),
    'orange': ('#FE7B34', '#FE8543'),
    'red': ('#CB2431', '#D73A49'),
}

COLOR_RANGES = [
    (90, 'green'),
    (75, 'yellowgreen'),
    (60, 'yellow'),
    (40, 'orange'),
    (0, 'red'),
]


def get_color(total: int) -> str:
    for range_, color in COLOR_RANGES:
        if total >= range_:
            return COLORS[color]

    raise ValueError('total cannot be negative')


def get_badge(total: int, color: str) -> str:
    template = (TEMPLATES_PATH / 'badge.svg').read_text(encoding='utf-8')
    template = template.replace('{{ total }}', str(total))
    template = template.replace('{{ color_dark }}', color[0])
    return template.replace('{{ color_light }}', color[1])


def save_badge(badge: str, outpath: Path) -> None:
    (outpath / 'badge.svg').write_text(badge, encoding='utf-8')


def make_badge(total: int, outpath: Path) -> None:
    color = get_color(total)
    badge = get_badge(total, color)
    save_badge(badge, outpath)
