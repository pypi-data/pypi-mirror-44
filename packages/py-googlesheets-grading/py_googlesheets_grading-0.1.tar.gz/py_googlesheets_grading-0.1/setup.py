from distutils.core import setup
setup(
  name = 'py_googlesheets_grading',         # How you named your package folder (MyLib)
  packages = ['py_googlesheets_grading'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Grades Gitlab stuff for you lmao',   # Give a short description about your library
  author = 'Jarle H. Wallevik',                   # Type in your name
  author_email = 'jovlisen@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/Zylvian/py_googlesheets_grading',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Zylvian/py_googlesheets_grading/archive/0.1.tar.gz',    # I explain this later on
  keywords = ['grading','google','sheets','gsheets'],   # Keywords that define your package best
  install_requires=[  # I get to this in a second
          'pygsheets',
          'Repo'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)