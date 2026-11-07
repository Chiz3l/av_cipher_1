import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'cipher_node'

setup(
    name=package_name,
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    entry_points={
        'console_scripts': [
            'cipher_server = caesar_cipher_py.cipher_server_node:main',
            'cipher_solver = caesar_cipher_py.cipher_solver_node:main',
        ],
    },
)