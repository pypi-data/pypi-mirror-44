from distutils.core import setup

setup(
    name="cellular_automaton",
    version="0.1.2",
    author="Richard Feistenauer",
    author_email="r.feistenauer@web.de",
    packages=["cellular_automaton"],
    url="https://gitlab.com/DamKoVosh/cellular_automaton",
    license="LICENSE.txt",
    description="N dimensional cellular automaton with multi processing capability.",
    long_description="README.md",
    long_description_content_type='text/markdown',
    requires=["pygame"]
)
