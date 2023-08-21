from setuptools import setup, find_packages
from typing import List

def get_requirements() ->List[str]:
    
    """
    This function will return list of requirements
    """
    requirement_list:List[str] = []
    
    
    return requirement_list

setup(
    name = 'sensor-fault-detection',
    version = '0.0.1',
    author = 'nishantborkar',
    author_email = 'nishantborkar139@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements(),#['pymongo'==3.54],
)