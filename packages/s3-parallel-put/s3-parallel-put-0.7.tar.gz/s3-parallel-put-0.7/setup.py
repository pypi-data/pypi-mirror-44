from setuptools import setup, find_packages

with open("README.md") as fh:
  long_description = fh.read()

setup(name='s3-parallel-put',
      version='0.7',
      description='s3-parallel-put Parallel uploads to Amazon AWS S3',
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
      ],
      keywords='s3 parallel',
      url='https://github.com/mishudark/s3-parallel-put',
      author='mishudark',
      # author_email='flyingcircus@example.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        "boto>=2.49.0",
        "python-magic>=0.4.15",
        "python-magic-bin>=0.4.14"
       ],
      entry_points={
        'console_scripts': ['s3-parallel-put=s3_parallel_put.s3_parallel_put:main']
      },
      )
