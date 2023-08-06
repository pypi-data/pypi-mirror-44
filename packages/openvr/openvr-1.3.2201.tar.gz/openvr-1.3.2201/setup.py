#!/bin/env python

from setuptools import setup

# Load module version from ovr/version.py
exec(open('src/openvr/version.py').read())

setup(
    name='openvr',
    version=__version__,
    author='Christopher Bruns and others',
    author_email='cmbruns@rotatingpenguin.com',
    description='Valve OpenVR SDK python bindings using ctypes',
    long_description='Valve OpenVR SDK python bindings using ctypes',
    url='https://github.com/cmbruns/pyopenvr',
    download_url='https://github.com/cmbruns/pyopenvr/tarball/' + __version__,
    package_dir={'': 'src'},
    packages=['openvr', 'openvr.glframework'],
    package_data={'openvr': ['*.dll', '*.so', '*.dylib']},
    keywords='openvr valve htc vive vr virtual reality 3d graphics',
    license='BSD',
    classifiers="""\
Environment :: Win32 (MS Windows)
Intended Audience :: Developers
License :: OSI Approved :: BSD License
Operating System :: Microsoft :: Windows
Operating System :: Microsoft :: Windows :: Windows 7
Operating System :: Microsoft :: Windows :: Windows 10
Operating System :: POSIX :: Linux
Operating System :: MacOS :: MacOS X
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.5
Programming Language :: Python :: 3.6
Programming Language :: Python :: Implementation :: CPython
Topic :: Multimedia :: Graphics :: 3D Rendering
Topic :: Scientific/Engineering :: Visualization
Development Status :: 4 - Beta
""".splitlines(),
    install_requires=[],
    extras_require={
        'all': ['numpy', 'PyOpenGL', 'glfw', 'PyQt5', 'jinja2', 'wxPython'],
        'glfw': ['numpy', 'PyOpenGL', 'glfw'],
        'opengl': ['numpy', 'PyOpenGL'],
        'PyQt5': ['numpy', 'PyOpenGL', 'PyQt5', 'jinja2'],
        #'PySide': ['PySide'], # does not support past python 3.5
        'wx': ['numpy', 'PyOpenGL', 'wxPython'],
    }
)
