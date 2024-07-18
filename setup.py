from setuptools import find_packages, setup
from typing import List


'''create function to integrate us_visa as an local package'''
HYPEN_E_DOT = '-e .'
def get_requirements(filepath:str)->List[str]:
    """
    This Function is responsible for handling packages requirements
    """
    requirements = []
    with open(filepath) as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace("/n","") for i in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements





setup(
    name="US-Visa-Project",
    version="0.0.1",
    author="Lavish",
    author_email="Lavishgangwani22@gmail.com",
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)