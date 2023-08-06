from distutils.core import setup

VERSION = '0.1.3'

setup(
    name='InANutshell',
    version=VERSION,
    author='Josh Prakke',
    author_email='joshprakke@gmail.com',
    url='https://github.com/JPrakke/in-a-nutshell',
    install_requires=['pyperclip == 1.7.0',],
    packages=['nutshell',],
    license='MIT License',
    description='makes meme text',
    long_description=open('README.txt').read(),
    entry_points = {
        'console_scripts':[
            'nutshell=nutshell:run'
        ]
    }
)


# Entry point format is terminal_command_name=python_script_name:main_method_name

