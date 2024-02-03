#!/usr/bin/env python3
import os

from setuptools import setup

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def get_version():
    """Find the version of the package"""
    version = None
    version_file = os.path.join(BASEDIR, "ovos_phal_plugin_aiy_v2", "version.py")
    major, minor, build, alpha = (None, None, None, None)
    with open(version_file, encoding="utf8") as f:
        for line in f:
            if "VERSION_MAJOR" in line:
                major = line.split("=")[1].strip()
            elif "VERSION_MINOR" in line:
                minor = line.split("=")[1].strip()
            elif "VERSION_BUILD" in line:
                build = line.split("=")[1].strip()
            elif "VERSION_ALPHA" in line:
                alpha = line.split("=")[1].strip()

            if (major and minor and build and alpha) or "# END_VERSION_BLOCK" in line:
                break
    version = f"{major}.{minor}.{build}"
    if alpha and int(alpha) > 0:
        version += f"a{alpha}"
    return version


def package_files(directory):
    paths = []
    for path, _, filenames in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join("..", path, filename))
    return paths


def required(requirements_file):
    """Read requirements file and remove comments and empty lines."""
    with open(os.path.join(BASEDIR, requirements_file), "r", encoding="utf8") as f:
        requirements = f.read().splitlines()
        if "MYCROFT_LOOSE_REQUIREMENTS" in os.environ:
            print("USING LOOSE REQUIREMENTS!")
            requirements = [
                r.replace("==", ">=").replace("~=", ">=") for r in requirements
            ]
        return [pkg for pkg in requirements if pkg.strip() and not pkg.startswith("#")]


def get_description():
    with open(os.path.join(BASEDIR, "README.md"), "r", encoding="utf8") as f:
        long_description = f.read()
    return long_description


PLUGIN_ENTRY_POINT = "ovos-phal-plugin-aiy-v2=ovos_phal_plugin_aiy_v2:AiyV2Plugin"
setup(
    name="ovos-phal-plugin-aiy-v2",
    version=get_version(),
    description="A plugin to handle Google AIY Voice Kit V2 button and LED",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/smartgic/ovos-phal-plugin-aiy-v2",
    author="Gaëtan Trellu (goldyfruit)",
    author_email="gaetan.trellu@gmail.com",
    license="Apache-2.0",
    packages=["ovos_phal_plugin_aiy_v2"],
    package_data={"": package_files("ovos_phal_plugin_aiy_v2")},
    install_requires=required("requirements.txt"),
    zip_safe=True,
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    entry_points={"ovos.plugin.phal": PLUGIN_ENTRY_POINT},
)
