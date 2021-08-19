import setuptools

with open('README.md') as readme:
    long_desc = readme.read()

setuptools.setup(
    name='pillar-youtube-upload',
    version='0.3.0',
    author="PillarGG",
    author_email='opensource@pillar.gg',
    description='Upload YouTube videos from Python and more.',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/pillargg/youtube-upload',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'httplib2>=0.18.1',
        'google-auth>=1.22.1',
        'google-api-core>=1.23.0',
        'google-api-python-client>=1.12.5',
        'oauth2client>=4.1.3'
    ]
)
