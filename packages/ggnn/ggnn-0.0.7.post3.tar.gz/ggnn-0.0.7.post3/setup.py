from setuptools import setup

setup(
    name='ggnn',
    version='0.0.7-3',
    license='Apache 2.0',
    author='Yijun Yu',
    author_email='y.yu@open.ac.uk',
    url='https://bitbucket.org/yijunyu/fast',
    long_description=('Generating Gated Graph Neural Networks from flat AST'
                      'serialization format.'),
    packages=['utils', 'utils.data', 'ggnn'],
    include_package_data=True,
    entry_points={'console_scripts': [
        "live_test=ggnn.live_test:main"]},
    install_requires=['flatast', 'tqdm'],
    requires=['flatast', 'tqdm', 'numpy', 'tensorboardX', 'sklearn', 'torch'],
    description='Gated Graph Neural Networks',
)
