from setuptools import setup, find_packages

setup(
    name = "Selector",
    version = "0.5.0",
    packages = find_packages(exclude=["tests"]),
    author = "Alexei Bendebury",
    author_email = "alexeibendebury@gmail.com",
    description = "An autodownloader for rinse.fm podcasts.",
    entry_points = {
        "console_scripts": [
            "selector = selector.selector:main",
        ],
    },
    classifiers = [
        "Programming Language :: Python :: 3"
    ],
    url="https://github.com/PlasmaSheep/selector",
    install_requires = ["PyYAML"],
    tests_require = ["nose", "coverage"],
    test_suite = "nose.collector",
    package_data = {
        '': ["*.yaml"],
        'selector': ["*.yaml"],
    }
)

