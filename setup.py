from setuptools import setup

setup(
    name='accountant',
    version='0.1',
    packages=['accountant', 'accounts', 'apis'],
    url='https://github.com/mateuszkulig/accountant',
    license='GNU General Public License v3.0',
    author='Mateusz Kulig',
    author_email='mateusz.kulig02@gmail.com',
    description='Tool written in python to make bot and web accounts easy to create.',
    install_requires=["selenium", "fng_api", "pyautogui", "urllib3"]
)
