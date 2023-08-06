from distutils.core import setup
setup(
  name = 'feather_nlp',
  version = '0.1.4',
  license='MIT',
  description = 'This library works on top of RASA-NLU to make its nlu functionalities \navailable in low powered devices like raspberry pi',   # Give a short description about your library
  author = 'Chidhambararajan',                   
  author_email = 'chidha1434@protonmail.com',
  url = 'https://github.com/Chidhambararajan/feather_nlp',
  download_url = 'https://github.com/Chidhambararajan/feather_nlp/archive/master.zip',
  keywords = ['NLP', 'machine learning', 'rasa nlu'],
  install_requires=[
          'rasa_nlu',
          'fuzzywuzzy[speedup]'
      ],
  classifiers=[
    'Development Status :: 4 - Beta ',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
