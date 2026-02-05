from setuptools import setup, find_packages

setup(
    name="topsis_chakshugupta_102303931",
    version="0.0.4",
    author="Your Name",
    author_email="youremail@gmail.com",
    description="TOPSIS implementation",
    packages=find_packages(),
    install_requires=["pandas", "numpy"],
    entry_points={
        'console_scripts': [
            'topsis=topsis.topsis:main'
        ]
    }
)
