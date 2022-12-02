from setuptools import find_packages, setup

# Add install requirements
setup(
    author="Heather",
    description="""A package to generate dataquilt visualizations\\
    based on weather data.""",
    name="dataquilt",
    version="0.0.1",
    packages=find_packages(where="src", include=["dataquilt", "data"]),
    package_dir={"": "src"},
    package_data={"data": ["*.txt", "*.csv", ".ase"]},
    # version="0.1.0",
    # install_requires=["numpy>=1.18.0", "numpy-financial>=1.0.0", "pandas"],
    # python_requires=">=3.6",
)
