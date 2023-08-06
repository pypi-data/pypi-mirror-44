from setuptools import setup


setup(
    name="tartarus",
    version="0.1",
    py_modules=['tartarus'],
    install_requires=[
        'Click',
        'colorama',
        'hexrec',
    ],

    entry_points={
        'console_scripts':
        'tartarus=tartarus:cli'

    }

)
