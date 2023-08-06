from distutils.core import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(this_directory, "LICENSE.txt"), encoding='utf-8') as f:
    license = f.read()

setup(
    name="cellular_automaton",
    version="0.1.3",
    author="Richard Feistenauer",
    author_email="r.feistenauer@web.de",
    packages=["cellular_automaton"],
    url="https://gitlab.com/DamKoVosh/cellular_automaton",
    license=license,
    description="N dimensional cellular automaton with multi processing capability.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    requires=["pygame"]
)
