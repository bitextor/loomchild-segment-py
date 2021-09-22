#!/usr/bin/env python

import setuptools
import subprocess
import os
import shutil
from sys import argv

__version__ = "2.0.4"

def compile_loomchild(current_path):
    jars = ["commons-cli-1.2.jar",  "commons-logging-1.2.jar",
        "gson-2.8.0.jar",  "hamcrest-core-1.3.jar", "jakarta.activation-1.2.2.jar",
        "jakarta.xml.bind-api-2.3.3.jar", "javax.activation-api-1.2.0.jar",
        "jaxb-api-2.3.1.jar",  "jaxb-core-2.3.0.1.jar", "jaxb-impl-2.3.3.jar",
        "junit-4.13.1.jar",  f"segment-{__version__}-SNAPSHOT.jar",
        f"segment-{__version__}-SNAPSHOT-tests.jar",  f"segment-ui-{__version__}-SNAPSHOT.jar"]

    all_compiled = True
    for f in jars:
        if not os.path.isfile(os.path.join(current_path, "loomchild/data/segment-2.0.4-SNAPSHOT/lib", f)):
            all_compiled = False
            break

    if not all_compiled:
        subprocess.check_call(["mvn", "clean", "install"], cwd=os.path.join(current_path, "segment/segment"))
        subprocess.check_call(["mvn", "clean", "install"], cwd=os.path.join(current_path, "segment/segment-ui"))
        subprocess.check_call(["unzip", "-o", os.path.join(current_path, f"segment/segment-ui/target/segment-{__version__}-SNAPSHOT.zip"),
            f"segment-{__version__}-SNAPSHOT/lib/*", "-d", os.path.join(current_path, "loomchild/data")])

    src_dir = os.path.join(current_path, "segment/srx")
    dst_dir = os.path.join(current_path, "loomchild/data/srx")
    os.makedirs(dst_dir, exist_ok=True)
    for item in os.listdir(src_dir):
        if not os.path.isfile(f"{src_dir}/{item}"):
            continue
        shutil.copy(os.path.join(src_dir, item), os.path.join(dst_dir, item))

if __name__=="__main__":
    with open("README.md", "r") as fh:
        long_description = fh.read()
    with open("requirements.txt", "r") as rf:
        requirements = rf.read().splitlines()

    compile_loomchild(os.path.dirname(os.path.abspath(__file__)))

    setuptools.setup(
        name="loomchild-segment",
        version=__version__,
        install_requires=requirements,
        license="GNU General Public License v3.0",
        author="Prompsit Language Engineering",
        author_email="info@prompsit.com",
        maintainer="Marta Bañon, Elsa Sarrías",
        maintainer_email="mbanon@prompsit.com, esarrias@dlsi.ua.es",
        description="Python wrapper for Loomchild segmenter",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/zuny26/loomchild-segment-py",
        packages=["loomchild"],
        package_data={
            "loomchild": [
                f"data/segment-{__version__}-SNAPSHOT/lib/*.jar",
                "data/srx/*.srx"
            ]
        },
        classifiers=[
            "Environment :: Console",
            "Intended Audience :: Science/Research",
            "Programming Language :: Python :: 3.7",
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: POSIX :: Linux",
            "Topic :: Text Processing :: Linguistic",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ],
        project_urls={
            "loomchild-segment-py on GitHub": "https://github.com/zuny26/loomchild-segment-py",
            "Loomchild segment on GitHub": "https://github.com/mbanon/loomchild",
            "Bifixer on GitHub": "https://github.com/bitextor/bifixer",
            "Prompsit Language Engineering": "http://www.prompsit.com",
            "Paracrawl": "https://paracrawl.eu/"
             },
        scripts=["py-segment"]
    )
