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
import os


FILE_PATH = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_PATH = os.path.abspath(os.path.join(FILE_PATH, 'templates'))

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


def get_color(total):
    for range_, color in COLOR_RANGES:
        if total >= range_:
            return COLORS[color]


def get_badge(total, color):
    badge_template_path = os.path.join(TEMPLATES_PATH, 'badge.svg')
    with open(badge_template_path) as f:
        template = f.read()
    template = template.replace('{{ total }}', str(total))
    template = template.replace('{{ color_dark }}', color[0])
    template = template.replace('{{ color_light }}', color[1])
    return template


def save_badge(badge, outpath):
    with open(os.path.join(outpath, 'badge.svg'), 'w') as f:
        f.write(badge)


def make_badge(total, outpath):
    color = get_color(total)
    badge = get_badge(total, color)
    save_badge(badge, outpath)
