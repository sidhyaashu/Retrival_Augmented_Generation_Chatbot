from setuptools import find_packages, setup

setup(
    name='college_genai_project',  # Use snake_case for package names
    version='0.0.1',
    author='Asutosh Sidhya',
    author_email='ashutoshsidhya69@gmail.com',
    description='A GenAI project for college use cases',
    long_description=open('README.md').read(),  # Make sure to have a README.md file
    long_description_content_type='text/markdown',
    url='https://github.com/sidhyaashu/Retrival_Augmented_Generation_Chatbot.git',  # Optional project URL
    packages=find_packages(), 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change if using a different license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
)
