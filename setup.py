from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name = 'doit-network',
    description = "doit cmd plugin: create task's dependency-graph image",
    version = '0.1.0',
    license = 'MIT',
    author = 'Zhu Liu',
    url = 'https://github.com/liuzmeta/doit-network',
    long_description=long_description,
    long_description_content_type="text/markdown",

    py_modules=['doit_network'],
    install_requires = ['doit', 'networkx'],
    entry_points = {
        'doit.COMMAND': [
            'network = doit_network:NetowrkCmd'
        ]
    },

    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: Developers',
    ),
    keywords = "doit graph network",
)
