# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['rinse', 'rinse.cookies']

package_data = \
{'': ['*'],
 'rinse.cookies': ['init/*',
                   'init/{{cookiecutter.rinse_init_dir}}/bin/*',
                   'init/{{cookiecutter.rinse_init_dir}}/lib/cran/*',
                   'init/{{cookiecutter.rinse_init_dir}}/src/cran/*',
                   'init/{{cookiecutter.rinse_init_dir}}/tmp/*']}

install_requires = \
['click>=7.0,<8.0', 'cookiecutter>=1.6,<2.0']

entry_points = \
{'console_scripts': ['rinse = rinse.rinse:rinse']}

setup_kwargs = {
    'name': 'rinstall',
    'version': '0.2.3',
    'description': 'A configurable installer CLI for installing R from source (sudo and non-sudo).',
    'long_description': "# rinse\n\nA CLI for installing R.\n\nCurrently works with:\n\n* __Repos__: CRAN\n* __Installation Methods__: Source\n* __Supported OS__: Linux\n* __Permission Level__: Sudo, Non-sudo\n\nWill work with:\n\n* __Repos__: Microsoft R Open\n* __Installation Methods__: Spack, Local\n* __Supported OS__: MacOS, Windows\n\n## Installation\n\nCurrently, rinse is in the alpha stage of development.  The latest release can be installed from PyPI\nor the development version can be installed from the *dev-master* branch on GitHub.\n\n### Latest Release\n\n```console\n[ $ ] pip install rinstall\n```\n### Development Version\n\nCreate a VE called `rinse` using your tool of choice:\n\n* pyenv\n* poetry\n* pipenv\n* virtualenv\n* virtualenvwrapper\n* conda\n* pew\n* python -m venv\n\nAfter making a VE install poetry into it:\n\n```console\n[ $ ] python -m venv ~/.env/rinse\n[ $ ] source ~/.env/rinse/bin/activate\n(rinse) [ $ ] pip install poetry\n...\n(rinse) [ $ ] mkdir GitHub; cd Github\n(rinse) [ ~/Github $ ] git clone -b dev-master https://github.com/datasnakes/rinse.git\n(rinse) [ ~/Github $ ] cd rinse\n(rinse) [ ~/Github/rinse $ ] poetry install\n...\n```\n\n### Initialize Rinse\n\nBefore you do anything, rinstall must be initialized or you will get an error:\n\n```console\n(rinse) [ ~/Github/rinse $ ] rinse init\n```\n\n## Simple Usage\n\nYou can install the latest version of R into your home directory with a single short command:\n\n```console\n(rinse) [ ~/Github/rinse $ ] rinse install\n# or\n(rinse) [ ~/Github/rinse $ ] rinse install latest\n# or\n(rinse) [ ~/Github/rinse $ ] rinse install 3.5.3\n```\n\n**Note**:  _Be aware that R can take around 20 minutes to install._\n\n## Alternate Usage\n\nFirst note:\n\n```console\n(rinse) [ ~/Github/rinse $ ] rinse configure --help # configure script help (./configure --help)\n# is different from\n(rinse) [ ~/Github/rinse $ ] rinse configure --chelp # rinse cli help\n```\n\nHere's how you can work through various installation steps:\n```console\n(rinse) [ ~/Github/rinse $ ] rinse configure 3.5.3\n(rinse) [ ~/Github/rinse $ ] rinse make --check 3.5.3\n(rinse) [ ~/Github/rinse $ ] rinse make --install 3.5.3 \n(rinse) [ ~/Github/rinse $ ] rinse make --install-tests 3.5.3\n(rinse) [ ~/Github/rinse $ ] rinse test --check --check-devel --check-all 3.5.3\n```\n\n## Maintainers\n\n* Kristen Bystrom\n* Rob Gilmore\n* Bruno Grande\n* Shaurita Hutchins\n",
    'author': 'Rob Gilmore',
    'author_email': 'robgilmore127@gmail.com',
    'url': 'https://github.com/datasnakes/rinse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)
