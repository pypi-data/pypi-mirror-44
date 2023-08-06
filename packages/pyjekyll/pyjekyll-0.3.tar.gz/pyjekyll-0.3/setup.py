from distutils.core import setup
setup(
  name = 'pyjekyll',
  packages = ['pyjekyll'], # this must be the same as the name above
  version = '0.3',
  description = 'A Jekyll Python library for handling Jekyll static sites',
  author = 'Stefan Nožinić',
  author_email = 'stefan@lugons.org',
  url = 'https://github.com/fantastic001/pyjekyll', # use the URL to the github repo
  download_url = 'https://github.com/fantastic001/pyjekyll/tarball/0.3', # I'll explain this in a second
  keywords = ["jekyll"], # arbitrary keywords
  package_dir = {'pyjekyll': 'src'},
  classifiers = [],
  install_requires=[] # dependencies listed here 
)
