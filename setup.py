from setuptools import setup

setup(
    name='lektor-static-search',
    version='0.1',
    author=u'Rafael Laverde,,,',
    author_email='leafar91@gmail.com',
    license='MIT',
    py_modules=['lektor_static_search'],
    entry_points={
        'lektor.plugins': [
            'static-search = lektor_static_search:StaticSearchPlugin',
        ]
    }
)
