from setuptools import find_packages, setup

# Add install requirements
setup(
    author="Heather",
    description="""A package that allows to generate dataquilt visualizations based on weather data.""",
    name="dataquilt",
    packages=find_packages(include=["dataquilt"]),
    version="0.1.0",
    install_requires=["numpy>=1.18.0", "numpy-financial>=1.0.0", "pandas"],
    python_requires=">=3.6",
)
