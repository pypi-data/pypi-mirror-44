from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='print_extended',
    version='0.2.0',

    description='Extended functionalities and better control '
                'over Python\'s built-in print function',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/arrrlo/print-extended',
    licence='MIT',

    author='Amphinicy Technologies ltd',
    author_email='info@amphinicy.com',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='python, print, extended',

    packages=find_packages(),
    install_requires=[
        'click~=7.0',
    ],

    project_urls={
        'Source': 'https://github.com/arrrlo/print-extended',
    },

    entry_points={
        'console_scripts': [
            'print_extended=print_extended.cli:cli'
        ],
    },
)
