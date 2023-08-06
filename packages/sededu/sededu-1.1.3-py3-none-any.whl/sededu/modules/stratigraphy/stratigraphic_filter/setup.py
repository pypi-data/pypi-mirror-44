from setuptools import setup
import re


# borrowed from Agile Scientific bruges tools
verstr = 'unknown'
VERSIONFILE = "stratigraphic_filter/_version.py"
with open(VERSIONFILE, "r") as f:
    verstrline = f.read().strip()
    pattern = re.compile(r"__version__ = ['\"](.*)['\"]")
    mo = pattern.search(verstrline)
if mo:
    verstr = mo.group(1)
    print("Version "+verstr)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
    name='stratigraphic_filter',
    version=verstr,
    author='Andrew J. Moodie',
    author_email='amoodie@rice.edu',
    packages=['stratigraphic_filter'],
    url='https://github.com/sededu/stratigraphic_filter',
    license='LICENSE.txt',
    description='educational activity for teaching about the stratigraphic filter',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3',
    include_package_data=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'Topic :: Education'],
    project_urls={
        'Bug Reports': 'https://github.com/sededu/stratigraphic_filter/issues',
        'Source': 'https://github.com/sededu/stratigraphic_filter',
    },
)
