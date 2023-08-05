import setuptools

setuptools.setup(
    name="gmail2json",
    version="2.5",
    author="Hudge",
    author_email="",
    description="",
    long_description="",
    long_description_content_type="text/markdown",
    url="",
    py_modules=["gmail2json"],
    install_requires=[
        "google-api-python-client",
        "google-auth-httplib2",
        "google-auth-oauthlib",
        "google-auth",
        "mail-parser",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
