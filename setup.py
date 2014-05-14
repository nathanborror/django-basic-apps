import os
from distutils.core import setup


def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == "":
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)


package_dir = "basic"


packages = []
for dirpath, dirnames, filenames in os.walk(package_dir):
    # ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith("."):
            del dirnames[i]
    if "__init__.py" in filenames:
        packages.append(".".join(fullsplit(dirpath)))

template_patterns = [
    'templates/*.html',
    'templates/*/*.html',
    'templates/*/*/*.html',
]

package_data = dict(
    (package_name, template_patterns)
    for package_name in packages
)

setup(name='django-basic-apps',
    version='0.7',
    description='Django Basic Apps',
    author='Nathan Borror',
    url='http://github.com/nathanborror/django-basic-apps',
    packages=packages,
    package_data=package_data)
