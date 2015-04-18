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
