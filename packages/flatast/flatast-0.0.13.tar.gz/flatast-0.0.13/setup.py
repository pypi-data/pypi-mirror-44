from setuptools import setup
setup(
    name='flatast',
    version='0.0.13',
    license='Apache 2.0',
    author='Yijun Yu',
    author_email='y.yu@open.ac.uk',
    url='https://bitbucket.org/yijunyu/fast',
    long_description=('Python runtime library for flat AST'
                      'serialization format.'),
    packages=['fast_', 'fast_.Data_', 'fast_.Graph_', 'fast_.Data_', 'flatast'],
    include_package_data=True,
    entry_points={'console_scripts': [
        'ggnn=flatast.flatast2ggnn:main'
        ]},
    install_requires=['flatbuffers', 'protobuf'],
    requires=['flatbuffers', 'protobuf'],
    description='Converting Flattened AST to Gated Graph Neural Networks',
)
