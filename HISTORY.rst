.. :changelog:

History
-------

0.1.0 (2013-10-08)
++++++++++++++++++

* First release.

0.1.1 (2013-10-11)
++++++++++++++++++

* Added support for custom adf.ly domains via the type='adfly' variable.

0.1.2 (2013-10-11)
++++++++++++++++++

* Fixed bug with t.co not working.

0.1.3 (2013-10-11)
++++++++++++++++++

* Added a timeout parameter

0.1.4 (2013-10-12)
++++++++++++++++++

* Added support for p.ost.im.
* Fixed blocking issue with direct links to file downloads

0.1.6 (2014-02-01)
++++++++++++++++++

* Fixed adfoc.us issues resulting from changes to their site
* Fixed linkbucks.com issues resulting from changes to their site

0.1.7 (2014-02-03)
++++++++++++++++++

* Fixed linkbucks.com issues resulting from additional changes to their site

0.1.8 (2014-02-04)
++++++++++++++++++

* Fixed linkbucks.com issues resulting from additional changes to their site

0.1.9 (2014-02-08)
++++++++++++++++++

* Switched linkbucks.com to use selenium PhantomJS driver due to ongoing challenges with their site

0.2.0 (2014-02-25)
++++++++++++++++++

* Removed PyV8 requirement for adf.ly
* Added ay.gy domain for adf.ly regex
* Added sh.st support

0.2.1 (2014-05-18)
++++++++++++++++++

* Removed tests for linkbucks.com and adfoc.us. Support has been temporarly
  removed.
* Merged Debian Python 3.2 fix by anaconda

0.2.2 (2014-07-28)
++++++++++++++++++

* Removed lnx.lu as site is out of service

0.2.3 (2015-11-13)
++++++++++++++++++

* Fixed sh.st support

0.3.0 (2016-05-20)
++++++++++++++++++

* Split out unshortening and unwrapping 301 redirects into separate calls.
* Added support for unwrapping google proxy links.
* Some general cleanup in tests, updated some of the test links.
* Handle anonymz.com links (provided by @guigarfr)
* Handle href.li links (provided by @guigarfr)
* Update user-agents (provided by @Dreysman)
