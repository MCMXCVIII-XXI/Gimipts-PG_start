from setuptools import setup, find_packages

setup(
    name='gimipts_project',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[

    ],
    entry_points={
        'console_scripts': [
            'gimipts=gimipts_project.run:run_ansible',
            'gimipts-pass=gimipts_project.run_pass:run_ansible'
        ],
    },
    author='Ilya Gimaletdinov',
    author_email='mcmxcviii@internet.ru',
    python_requires='>=3.13',
)
