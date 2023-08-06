import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='treeview',  
    version='1.1.3',
    scripts=['treeview'] ,
    author="Low Yiyiu",
    author_email="lowyiyiu@gmail.com",
    description="Folder Strucutre Visualizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lowyiyiu/treeview",
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').read().splitlines(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
 )