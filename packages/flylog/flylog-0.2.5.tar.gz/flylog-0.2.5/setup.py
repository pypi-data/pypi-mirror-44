from setuptools import setup, find_packages

setup(
    name="flylog",
    version='0.2.5',
    zip_safe=False,
    platforms='any',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    install_requires=['requests'],
    scripts=['flylog/bin/run_flylog.py'],
    url="https://github.com/dantezhu/flylog",
    license="BSD",
    author="dantezhu",
    author_email="zny2008@gmail.com",
    description="make log fly to mail or other",
)
