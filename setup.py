from setuptools import setup, find_packages

VERSION = '1.0.3' 
DESCRIPTION = 'remoteio - Remote GPIO control '
LONG_DESCRIPTION = 'A Raspberry Pi GPIO remote control based on gpiozero'


setup(
        name="remoteio", 
        version=VERSION,
        author="Christoph Scherbeck",
        author_email="christoph@scherbeck.tech",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["gpiozero"], 
        
        keywords=['python', 'remoteio'],
        classifiers= [
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
            "Operating System :: POSIX :: Linux",
            "Environment :: Other Environment",
            "Intended Audience :: Developers",
            "Intended Audience :: Education",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Topic :: System :: Hardware",
        ],
        project_urls={
        'Homepage': 'https://github.com/schech1/remoteio'
    }
)