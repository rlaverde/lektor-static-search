from setuptools import setup

setup(
    name='lektor-tipue-search',
    version='0.1',
    author=u'Rafael Laverde,,,',
    author_email='leafar91@gmail.com',
    license='MIT',
    py_modules=['lektor_tipue_search'],
    entry_points={
        'lektor.plugins': [
            'tipue-search = lektor_tipue_search:TipueSearchPlugin',
        ]
    }
)
