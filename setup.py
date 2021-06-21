import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(
    name="robotframework-notifications",
    version="1.2.0",
    description="Send notifications to Slack or Mattermost using Robot Framework.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/tlolkema/RobotNotifications",
    author="Tim Lolkema",
    author_email="tim@detesters.nl",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["RobotNotifications"],
    include_package_data=True,
    install_requires=["requests"],
)
