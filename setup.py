from setuptools import setup, find_packages

setup(
    name='ifindex',  # 包名
    version='0.0.1',  # 版本
    description="some index",  # 包简介
    long_description=open('README.md').read(),  # 读取文件中介绍包的详细内容
    include_package_data=True,  # 是否允许上传资源文件
    author='haifan',  # 作者
    author_email='',  # 作者邮件
    maintainer='',  # 维护者
    maintainer_email='',  # 维护者邮件
    license='MIT License',  # 协议
    url='',  # github或者自己的网站地址
    packages=find_packages(),  # 包的目录
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',  # 设置编写时的python版本
    ],
    python_requires='>=3.7',  # 设置python版本要求
    install_requires=[''],  # 安装所需要的库
    # entry_points={
    #     'console_scripts': [
    #         ''],
    # },  # 设置命令行工具(可不使用就可以注释掉)
)