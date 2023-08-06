from setuptools import setup

setup(
    name="jshort",
    version="1.0.0",
    py_modules=["jshort"],
    description="Json shorthand for python",
    author="Eric Régnier",
    author_email="utopman@gmail.com",
    license="MIT",
    install_requires=["pygments", "jsonpath-ng"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: Jython",
        "Intended Audience :: Developers",
    ],
    keywords=["utility", "json", "tool"],
    url="http://github.com/eregnier/j",
)
