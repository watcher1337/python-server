from setuptools import setup

setup(
    name="python-server",
    version="1.0.0",
    py_modules=["python_server"],  # Match the import name
    install_requires=[
        "netifaces>=0.11.0",
    ],
    entry_points={
        "console_scripts": [
            "python-server=python_server:main",
        ],
    },
    author="your-username",
    description="HTTP file server with upload support and authentication",
    url="https://github.com/your-username/python-server",
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
