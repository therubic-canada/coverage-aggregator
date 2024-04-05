from setuptools import setup

package_name = 'coverage-aggregator'

setup(
    name=package_name,
    version='0.1.1',
    description='Coverage report aggregator',
    packages=['coverage_aggregator'],
    install_requires=['setuptools', 'jinja2'],
    zip_safe=True,
    package_data={'coverage_aggregator': ['templates/*', 'static/*']},
    maintainer='Auguste Lalande',
    maintainer_email='alal@therubic.com',
    entry_points={
        'console_scripts': [
            'aggregate-coverage-reports = '
            'coverage_aggregator.aggregator:aggregate',
        ],
    },
)
