import codecs
import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()

about = {}
with open(os.path.join(here, "doodledashboard", "__about__.py")) as f:
    exec(f.read(), about)

setup(
    name=about["__name__"],
    version=about["__version__"],
    description="Extensible dashboard designed to display data from multiple sources.",
    long_description=long_description,
    url="https://github.com/SketchingDev/Doodle-Dashboard",
    license="MIT",
    packages=find_packages(exclude=["tests", "examples"]),
    install_requires=[
        "requests",
        "slackclient",
        "feedparser",
        "pyyaml>=4.2b1",
        "click",
        "image-to-ascii-converter",
        "ratelimit"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "doodledashboard=doodledashboard.cli:cli"
        ],
        "doodledashboard.custom.displays": [
            "console=doodledashboard.displays.console:ConsoleDisplayConfig"
        ],
        "doodledashboard.custom.filters": [
            "contains-text=doodledashboard.filters.contains_text:ContainsTextFilterConfig",
            "matches-regex=doodledashboard.filters.matches_regex:MatchesRegexFilterConfig"
        ],
        "doodledashboard.custom.datafeeds": [
            "datetime=doodledashboard.datafeeds.datetime:DateTimeFeedConfig",
            "rss=doodledashboard.datafeeds.rss:RssFeedConfig",
            "slack=doodledashboard.datafeeds.slack:SlackFeedConfig",
            "text=doodledashboard.datafeeds.text:TextFeedConfig"
        ],
        "doodledashboard.custom.notification": [
            "image-depending-on-content=doodledashboard.notifications.image.image:ImageDependingOnMessageContentConfig",
            "text-in-message=doodledashboard.notifications.text.text:TextInMessageConfig"
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.4"
    ],
    python_requires=">=3.4"
)
