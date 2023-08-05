=============================
Change log for gocept.package
=============================

3.1 (2019-04-01)
================

Regression
----------

- This package is currently not compatible with Sphinx >= 1.7.


3.0 (2018-01-25)
================

- Drop python 3.3 support as it is no longer supported by Sphinx 1.5.

- Change License to MIT License.


2.3 (2016-12-02)
================

- Ensure compatibility with `setuptools > 30.0`.


2.2 (2016-11-23)
================

- Support PyPy 2.


2.1 (2016-02-19)
================

- Use current `bootstrap.py` in the skeleton.


2.0 (2016-02-18)
================

- Updated bitbucket URLs of current changelog files.

- Drop support for Python 2.6.

- Support Python 3.3, 3.4, 3.5.

- Use tox as one and only testrunner.

- Update to Sphinx >= 1.3.


1.3 (2014-09-17)
================

- Add ``--pdf`` option to the ``bin/doc`` command.

- Added a template for a minimal web-app deployment using batou.

- Use py.test instead of zope.testrunner.


1.2 (2013-07-19)
================

- Added .mr.developer.cfg to the skeleton's .hgignore file.

- Development buildout is now required to run in a Python environment that has
  setuptools available.

- Use zc.buildout 2.x and current setuptools instead of distribute in response
  to the setuptools merge.

- Updated package versions.


1.1 (2013-06-04)
================

- Use pkginfo >= 0.9 which contains a fix for finding metadata of installed
  namespace packages (see <https://bugs.launchpad.net/pkginfo/+bug/934311>).

- Add example stanza for a console_script entrypoint to the skeleton setup.py.

- Updated Mercurial links to point to bitbucket.org.

- Updated link to online docs to point to pythonhosted.org.

- Updated home page and issue reporting to remove outdated assumptions about
  gocept's project hosting.

- Updated ZTK to 1.1.5, zc.buildout to 1.7.1.

- Pin zc.buildout and distribute during bootstrap.


1.0.1 (2012-04-20)
==================

- Add coveragerc to package skeleton.


1.0 (2012-02-24)
================

initial release
