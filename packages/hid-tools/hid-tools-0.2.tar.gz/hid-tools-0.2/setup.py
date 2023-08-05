#!/usr/bin/python3

import os
import sys
import io
from setuptools import setup
from setuptools.command.install import install


class ManPageGenerator(install):
    def run(self):
        man_pages = self.pandocify()
        if man_pages:
            entry = (os.path.join(self.prefix, 'share', 'man', 'man1'),
                     man_pages)
            self.distribution.data_files.append(entry)
        super().run()

    def pandocify(self):
        try:
            import pypandoc
            # pypandoc spews install instructions to stderr when it can't find
            # pandoc. So we redirect stderr and restore it with a saner
            # message.
            old_stderr = sys.stderr
            pandoc_found = True
            try:
                with io.StringIO() as s:
                    sys.stderr = s
                    pypandoc.get_pandoc_version()
            except OSError:
                pandoc_found = False
            finally:
                sys.stderr = old_stderr

            if not pandoc_found:
                print('*****************************************************\n'
                      'Pandoc man page conversion failed, skipping man pages\n'
                      '*****************************************************\n',
                      file=sys.stderr)
                return None

            # now do the actual conversion
            here = '.'
            mandir = os.path.join(here, 'man')
            man_pages = []
            for f in os.listdir(mandir):
                if f.endswith('.md'):
                    path = os.path.join(mandir, f)
                    outfile = f'{path[:-3]}.1'
                    pypandoc.convert_file(path, 'man',
                                          outputfile=outfile,
                                          extra_args=['-s'])
                    man_pages.append(outfile)
        except ModuleNotFoundError:
            print('*********************************************\n'
                  'Module pypandoc not found, skipping man pages\n'
                  '*********************************************\n',
                  file=sys.stderr)
            return None
        return man_pages


setup(name='hid-tools',
      version='0.2',
      description='HID tools',
      long_description=open('README.md', 'r').read(),
      url='http://gitlab.freedesktop.org/libevdev/hid-tools',
      packages=['hidtools', 'hidtools.cli'],
      author='Benjamin Tissoires',
      author_email='benjamin.tissoires@redhat.com',
      license='GPL',
      entry_points={
          'console_scripts': [
              'hid-decode= hidtools.cli.decode:main',
              'hid-recorder = hidtools.cli.record:main',
              'hid-replay = hidtools.cli.replay:main',
          ]
      },
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6'
      ],
      data_files=[],  # man pages are added on success
      python_requires='>=3.6',
      include_package_data=True,
      install_requires=['parse', 'pyudev'],
      cmdclass=dict(
          install=ManPageGenerator,
      )
      )
