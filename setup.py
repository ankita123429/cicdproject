from setuptools import find_packages,setup
from typing import List


HYPEN_E_DOT='-e.'
def get_requirements(file_path:str)->List[str]:
    '''
         This function will retuen a list of requirements
    '''
    requirements=[]
    with open (file_path) as file_obj:
        requirements=file_obj.readline()
        requirements=[req.replace("\n", "") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)


setup(
    name='cicdproject',
    version='0.0.1',
    author='ankita',
    author_email='ankita.kathed@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
    )
    