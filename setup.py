from setuptools import setup, find_packages

setup(
    name='LaCrema',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/stefanyuk/EPAM-Final-project',
    zip_safe=False,
    install_requires=[
        'Flask>=2.02',
        'Flask-Migrate>=3.1.0',
        'Flask-RESTful>=0.3.9',
        'Flask-SQLAlchemy>=2.5.1',
        'Flask-WTF>=1.0.0'
    ]
)
