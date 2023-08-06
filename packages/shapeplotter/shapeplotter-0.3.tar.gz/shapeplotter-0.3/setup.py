import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(name='shapeplotter',
                 version='0.3',
                 description='A simple library to plot shapely objects.',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='https://github.com/Extintor/shapeplotter',
                 author='Paul Charbonneau',
                 author_email='paulcharbo@gmail.com',
                 license='GPLv3',
                 packages=setuptools.find_packages(),
                 install_requires=['matplotlib', ],
                 zip_safe=False,
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
                     "Operating System :: OS Independent",
                     "Topic :: Scientific/Engineering :: Visualization",
                 ],
                 )
