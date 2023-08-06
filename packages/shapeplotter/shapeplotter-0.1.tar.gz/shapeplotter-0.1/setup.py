import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(name='shapeplotter',
      version='0.1',
      description='The funniest joke in the world',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/Extintor/shapeplotter',
      author='Paul Charbonneau',
      author_email='paulcharbo@gmail.com',
      license='GPL3',
      packages=setuptools.find_packages(),
      install_requires=[
          'matplotlib',
      ],
      zip_safe=False,
      classifiers=[
           "Programming Language :: Python :: 3",
           "License :: OSI Approved :: MIT License",
           "Operating System :: OS Independent",
      ],
                 )
