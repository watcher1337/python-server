from setuptools import setup

setup(
    name="python-server",
    version="1.0.1",  # <--- CHANGE THIS
    py_modules=["python_server"],
    install_requires=[
        "legacy-cgi>=2.6.4",
        "netifaces>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "python-server=python_server:main",
        ],
    },
    author="watcher1337",
    description="HTTP file server with upload support and authentication",
    url="https://github.com/watcher1337/python-server",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
