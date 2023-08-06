import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()


setuptools.setup(
    name='sgwc',
    version='2019.4.12',
    author='Czw_96',
    author_email='459749926@qq.com',
    description='搜狗微信文章爬虫',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Czw96/sgwc',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'lxml',
        'requests',
        'Pillow',
    ]
)
