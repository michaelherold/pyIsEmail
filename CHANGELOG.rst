2.0.0 (2022-10-17)
------------------

- **Breaking (Python 2):** Upgrade to the new ``dnspython`` resolve API for DNS checks for future-proofing [`229db4f`_] - `@moshfrid`_.
- **Breaking (Python 2):** Drop support for Python versions prior to 3.6 [`635aff4`_] - `@michaelherold`_.
- Consider emails with domains that have null MX records, per RFC7505, invalid when checking DNS [`ebc4a2f`] - `@bmcculley`_.

.. _229db4f: https://github.com/michaelherold/pyIsEmail/commit/229db4fe4f790b5a95e1e85bffbdd42464472ea5
.. _635aff4: https://github.com/michaelherold/pyIsEmail/commit/635aff42c3cd0a04f3bad8c79099cd5827fed74f
.. _ebc4a2f: https://github.com/michaelherold/pyIsEmail/commit/ebc4a2f8120b02d488472c1f5bf293b155b58118
.. _@moshfrid: https://github.com/moshfrid
.. _@bmcculley: https://github.com/bmcculley

1.4.0 (2021-09-16)
------------------

- Allow limiting of email addresses on Generic Top-Level Domains (gTLDs) with the ``allow_gtld=False`` option [`bf13a6c`_] - `@michaelherold`_.

.. _bf13a6c: https://github.com/michaelherold/pyIsEmail/commit/bf13a6cfe662e66c8c6a5a9228d80cacf901b1ba

1.3.2 (2018-07-05)
----------

- Upgrade to universal dnspython version - `@peterdemin`_.

.. _@peterdemin: https://github.com/peterdemin

1.3.1 (2015-09-18)
------------------

- Release as non-universal wheels because of the dnspython dependency.

1.3.0 (2015-04-18)
------------------

- Bugfix: Ensures that DNS checks fail context with or without
  a diagnosis [`c7b91f6`_] - `@michaelherold`_.
- The DNSValidator now fails checks when a query times out or fails to
  return a response from any nameserver [`f8f4af7`_] - `@michaelherold`_.

.. _c7b91f6: https://github.com/michaelherold/pyIsEmail/commit/c7b91f64b87b88a501628bb73cc6777b10e45ba5
.. _f8f4af7: https://github.com/michaelherold/pyIsEmail/commit/f8f4af7b4b2441c81a442f41b977ce8780f129a4

1.2.0 (2015-03-13)
------------------

- Removed dependency on pypandoc for building. This should fix any user
  installation issues [`60a4d6`_] - `@michaelherold`_.

.. _60a4d6: https://github.com/michaelherold/pyIsEmail/commit/60a4d65906736593a6c2547065ad0d5b0024aaec

1.1.0 (2014-07-14)
------------------

- Failed DNS checks now return DNSDiagnosis instead of RFC5322Diagnosis [`84d258`_] - `@michaelherold`_.

.. _84d258: https://github.com/michaelherold/pyIsEmail/commit/84d2581ef7dd7b222ae21bee0692a618a073e9c2

1.0.1 (2014-01-27)
------------------

- Little bits of cleanup [`8044aa`_] `@michaelherold`_.

.. _8044aa: https://github.com/michaelherold/pyIsEmail/commit/8044aa1132ecf7ebb6d7c72719d6ebb239cb3eba

1.0.0 (2013-10-30)
------------------

- Initial Release [`b8b885`_]  - `@michaelherold`_.

.. _@michaelherold: https://github.com/michaelherold
.. _b8b885: https://github.com/michaelherold/pyIsEmail/commit/b8b88598a244a48db8f00ff7d9860f09f984b7e1
