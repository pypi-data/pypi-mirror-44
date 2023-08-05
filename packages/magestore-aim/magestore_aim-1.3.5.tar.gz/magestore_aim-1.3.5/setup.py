import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

package_name = 'magestore_aim'
packages = setuptools.find_packages(include=[package_name, "{}.*".format(package_name)])

setuptools.setup(
    name=package_name,
    version="1.3.5",
    author="Mars",
    author_email="mars@trueplus.vn",
    description="Fix web port range v5",
    long_description=long_description,
    long_description_content_type="",
    url="https://github.com/Magestore/go-environment",
    packages=packages,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires='>=3',
    install_requires=[
        # install specific crytography 2.4.2 to fix error with 2.5 version
        # ref: https://github.com/paramiko/paramiko/issues/1369
        'cryptography==2.4.2',
        'fabric',
    ]
)
