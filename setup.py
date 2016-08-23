from setuptools import setup, find_packages
import os

version = '1.0.0.dev0'

setup(
    name='bccvl_tools',
    version=version,
    description="BCCVL Tools",
    # long_description=open("README.txt").read() + "\n" +
    #                  open(os.path.join("docs", "HISTORY.txt")).read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
    ],
    keywords='',
    author='',
    author_email='',
    url='http://svn.plone.org/svn/collective/',
    license='GPL',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['bccvl_tools'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    entry_points={
        'console_scripts': [
            'generate_sdmbank_md = bccvl_tools.sdmbank_tools.generate_sdmbank_metadata:main',
            'run_sdmdemo = bccvl_tools.sdmbank_tools.run_sdmdemo:main',
        ]
    }
    )
