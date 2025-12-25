from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='pywinauto-pytest',
    version='0.1.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A pytest plugin for pywinauto UI automation testing, supporting multiple test case formats and Allure reporting',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/walkzzz/pywinauto-pytest',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'flake8>=5.0.0',
            'black>=23.0.0',
        ],
    },
    entry_points={
        'pytest11': [
            'pywinauto_pytest = pywinauto_pytest.plugin',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: User Interfaces',
    ],
    python_requires='>=3.7',
    include_package_data=True,
    zip_safe=False,
    keywords=['pytest', 'pywinauto', 'ui automation', 'testing', 'allure'],
)
