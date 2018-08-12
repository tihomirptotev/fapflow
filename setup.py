from setuptools import setup

setup(
    name='flask-apflow',
    entry_points={
        'console_scripts': [
            'apflow=apflow_flask.commands:proba'
        ],
    },
)
