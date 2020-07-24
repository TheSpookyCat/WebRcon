from setuptools import setup

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

with open('README.md', 'r') as fp:
    long = fp.read()

setup(name='webrcon',
      author='lewdneko',
      url='https://github.com/lewdneko/webrcon',
      version='1.0.1',
      packages=['webrcon'],
      setup_requires=['wheel'],
      python_requires='>=3.6',
      platforms=['Windows', 'Linux', 'OSX'],
      zip_safe=True,
      license='BlueOak-1.0.0',
      description='Basic async interface for Rust\'s WebRcon protocol',
      long_description=long,
      long_description_content_type='text/markdown',
      keywords='rust webrcon rcon websockets ws rust_game async',
      install_requires=install_requires
)
