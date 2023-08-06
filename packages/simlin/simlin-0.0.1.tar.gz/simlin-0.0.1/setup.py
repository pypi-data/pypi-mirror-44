from setuptools import setup

version = '0.0.1'

setup(name='simlin',
      version=version,
      description='Simple Image Manipulator for Linux',
      long_description=open("./README.md", "r").read(),
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: End Users/Desktop",
          "Natural Language :: English",
          "Operating System :: POSIX :: Linux",
          "Programming Language :: Python :: 3",
          "Topic :: Multimedia :: Graphics :: Graphics Conversion",
          "License :: OSI Approved :: MIT License",
          ],
      author='Al Audet',
      author_email='alaudet@linuxnorth.org',
      url='https://www.linuxnorth.org/simlin/',
      download_url='https://github.com/alaudet/simlin/releases',
      license='MIT License',
      packages=['simlin'],
      scripts=['bin/simlin'],
      install_requires=['pillow']
      )
