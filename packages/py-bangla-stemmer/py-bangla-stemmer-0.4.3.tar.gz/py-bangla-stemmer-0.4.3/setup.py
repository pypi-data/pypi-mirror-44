from distutils.core import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='py-bangla-stemmer',  # How you named your package folder (MyLib)
    packages=['py_bangla_stemmer', 'py_bangla_stemmer.stemmer', 'py_bangla_stemmer.resources'],  # Chose the same as "name"
    version='0.4.3',  # Start with a small number and increase it with every change you make
    license='GPL-3.0',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='Rule based Bengali Stemmer written in python',  # Give a short description about your library
    long_description=readme(),  # Give a short description about your library
    author='Sazedul Islam',  # Type in your name
    author_email='sazidmailbox@gmail.com',  # Type in your E-Mail
    url='https://github.com/sazid1462/py-bangla-stemmer',  # Provide either the link to your github or to your website
    download_url='https://github.com/sazid1462/py-bangla-stemmer/archive/0.4.3.tar.gz',  # I explain this later on
    keywords=['stemmer', 'bengali-stemmer', 'bangla-stemmer', 'rule-based-stemmer', 'nlp'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Natural Language :: Bengali',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
    ],
)
