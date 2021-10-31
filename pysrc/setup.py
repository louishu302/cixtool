from distutils.core import setup, Extension
moduele1 = Extension(
    name         ='tool',
    define_macros=[('MAJOR_VERSION','1'),
                    ('MINOR_VERSION','0')],
    include_dirs= ['/home/lohu/workspace/cixtool/include'],
    libraries   = ['hosttest'],
    library_dirs= ['/home/lohu/workspace/cixtool/lib'],
    sources     = ['/home/lohu/workspace/cixtool/src/wrapper.cpp'],
    language    = "c++"


)

setup(
    name= 'tool',
    version= '1.0',
    description= 'This is a powerful tool',
    author= 'Martin-Vis',
    author_email='Martin-Vis@v.loewis.de',
    url= 'https://docs.python.org/extending/building',
    long_description='This is really a powerful tool',
    ext_modules= [moduele1]
)


#setup(name='tool',version='1.0', ext_modules=[Extension('tool',['wrapper.c'])])

# create and distribute python module by command line-
# python setup.py build_ext --inplace   : place extension to current folder with
#                                         source together 
# 
# In Python scripting, following contributions
# vscode.File->preference->settings: python.analysis.extrapath     
#     add path: /home/lohu/workspace/cixtool/pysrc/ 
# import tool
# print tool.spird() 