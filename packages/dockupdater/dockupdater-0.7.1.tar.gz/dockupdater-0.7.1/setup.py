from setuptools import find_packages
from setuptools import setup

from dockupdater import VERSION

requirements = [
    'docker>=3.7.0',
    'apscheduler>=3.5.3',
    'requests>=2.21.0',
    'apprise>=0.7.5',
    'jinja2>=2.10',
    'click>=7.0',
]


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name='dockupdater',
    version=VERSION,
    maintainer='Mathieu Cantin',
    maintainer_email='harcher81@gmail.com',
    description='Automatically keep your docker services and your docker containers up-to-date with the latest version',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://dockupdater.dev',
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    scripts=['entrypoint'],
    install_requires=requirements,
    python_requires='>=3.6.2',
)
