Overview
========

The MailHost product provides support for sending email from within the Zope
environment using MailHost objects.

An optional character set can be specified to automatically encode unicode
input, and perform appropriate RFC 2822 header and body encoding for the
specified character set. Full python email.Message.Message objects may be sent.

Email can optionally be encoded using Base64 or Quoted-Printable encoding
(though automatic body encoding will be applied if a character set is
specified).

Usage
-----

MailHost provides integration with the Zope transaction system and optional
support for asynchronous mail delivery. Asynchronous mail delivery is
implemented using a queue and a dedicated thread processing the queue. The
thread is (re)-started automatically when sending an email. The thread can be
started manually (in case of restart) by calling its
manage_restartQueueThread?action=start method through HTTP. There is currently
no possibility to start the thread at Zope startup time.

Supports TLS/SSL encryption (requires Python compiled with SSL support).

Configuration
-------------

To force MailHost to only queue mails without sending them, activate queuing
in the ZMI and set the environment variable ``MAILHOST_QUEUE_ONLY=1``.
This could be helpful in a staging environment where mails should not be sent.

Changelog
=========

4.4 (2019-04-03)
----------------

- Add ability to disable sending of queued mails. Details see README.rst.
  (`#14 <https://github.com/zopefoundation/Products.MailHost/issues/14>`_)


4.3 (2019-03-08)
----------------

- silence deprecation warning due to non-raw regex
  (`#13 <https://github.com/zopefoundation/Products.MailHost/issues/13>`_)

- Specify supported Python versions using ``python_requires`` in setup.py
  (`Zope#481 <https://github.com/zopefoundation/Zope/issues/481>`_)

- Add support for Python 3.8


4.2 (2018-10-05)
----------------

- Add icon for Bootstrap ZMI.

- Fix start-up in case ``Products.GenericSetup`` is not installed.
  (`#9 <https://github.com/zopefoundation/Products.MailHost/issues/9>`_)

- Add support for Python 3.7.


4.1 (2018-05-20)
----------------

- Fix GenericSetup support for GenericSetup 2.x

- Fix DeprecationWarnings

- PEP-8 code style compliance

- Drop support for Python 3.4


4.0 (2017-09-14)
----------------

- Move GenericSetup export/import support from the GenericSetup package
  to MailHost as a setuptools extra.

- Python 3 compatibility

- Require Zope 4, aka drop Zope 2.13 support.

- add test coverage reporting

- Use `@implementer` class decorator.

- Drop long-deprecated support for uuencoded emails.

3.0 (2016-07-18)
----------------

- Remove HelpSys support.

2.13.2 (2014-11-02)
-------------------

- Adjust tests to pass with latest zope.sendmail versions.

- Specify detailed distribution dependencies.

2.13.1 (2010-09-25)
-------------------

- LP #642728: Fixed TypeError on nested multi part messages in MailHost.

2.13.0 (2010-07-13)
-------------------

- Released as separate package.


