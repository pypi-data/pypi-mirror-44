import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='ikuzo-python',  
     version='0.1.4',
     author="Ikuzo",
     author_email="tohyongcheng@gmail.com",
     description="A library to quickly deploy machine learning models to the web",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
     install_requires=[
        'pubnub>=3,<4',
        'haikunator'
    ]
 )