from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name="cellular_automaton",
    version="0.2.0",
    author="Richard Feistenauer",
    author_email="r.feistenauer@web.de",
    packages=["cellular_automaton"],
    url="https://gitlab.com/DamKoVosh/cellular_automaton",
    license="Apache License 2.0",
    description="N dimensional cellular automaton with multi processing capability.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    requires=[],
    python_requires='>3.6.1'
)
