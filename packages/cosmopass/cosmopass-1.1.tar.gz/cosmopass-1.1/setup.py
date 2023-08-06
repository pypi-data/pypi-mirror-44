from distutils.core import setup
files = ["equations/*","likelihoods/*","likelihoods/Data/*"]
setup(
        name = 'cosmopass',
        packages = ['cosmopass'],
        package_data = {'cosmopass' : files },
        version = '1.1',
        description = 'COSMOlogical Parameterisation And Scalar field Solver',
        author = 'Anto I Lonappan',
        author_email = 'anto.lonappan@sissa.it',
        url = 'https://gitlab.com/antolonappan/cosmopass',
        )


