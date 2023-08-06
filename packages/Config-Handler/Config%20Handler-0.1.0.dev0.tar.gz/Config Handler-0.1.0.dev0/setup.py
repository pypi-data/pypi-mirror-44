from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Config Handler',
    version='0.1.0.dev0',

    description='Handle config files in your projects the easy way',
    long_description=readme(),
    long_description_content_type='text/markdown',

    url='https://github.com/amphinicy/config-handler.git',
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
    keywords='config, config-handler, python, json',

    packages=find_packages(),
    install_requires=[
        'click~=7.0',
    ],

    project_urls={
        'Source': 'https://github.com/amphinicy/config-handler.git',
    },

    entry_points={
        'console_scripts': [
            'config_handler=config_handler.cli:cli'
        ],
    },
)
