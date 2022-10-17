Contributing
============

In the spirit of `free software <http://www.fsf.org/licensing/essays/free-sw.html>`__, we encourage **everyone** to help improve this project. Here are some ways *you* can contribute:

- Use alpha, beta, and pre-release versions.
- Report bugs.
- Suggest new features.
- Write or edit documentation.
- Write specifications.
- Write code (**no patch is too small**: fix typos, add comments, clean up inconsistent whitespace).
- Refactor code.
- Fix `issues <https://github.com/michaelherold/pyIsEmail/issues>`__.
- Review patches.

Submitting an issue
-------------------

We use the `GitHub issue tracker <https://github.com/michaelherold/pyIsEmail/issues>`__ to track bugs and features. Before submitting a bug report or feature request, check to make sure no one else has already submitted the same bug report.

When submitting a bug report, please include a `Gist <https://gist.github.com>`__ that includes a stack trace and any details that may be necessary to reproduce the bug, including your pyIsEmail version, Python version, and operating system.

Ideally, a bug report should include a pull request with failing tests.

Writing code
------------

There is a setup script that you can run directly on any platform that has a POSIX shell. Run ``script/setup`` to get started, then skip to the next section. For more information, read on in this section.

We use `Hatch <https://hatch.pypa.io/1.6/>`__ to manage the project. It enables us to centralize the organization of our dependencies and development harness.

To get started with Hatch, you can `install it <https://hatch.pypa.io/1.6/install/>`__ in a variety of ways. We recommend installing it via your operating system's package manager or with ``pipx`` instead of using ``pip``.

Once you have installed Hatch, you are ready to started contributing code!

Submitting a pull request
-------------------------

1. Fork the repository.
2. Create a topic branch.
3. Add tests for your unimplemented feature or bug fix.
4. Run ``script/test``. If your tests pass, return to step 3.
5. Implement your feature or bug fix.
6. Run ``script/chores``. If your tests or any of the linters fail, return to step 5.
7. Open ``coverage/index.html``. If your changes are not fully covered by your tests, return to step 3.
8. Add documentation for your feature or bug fix.
9. Commit and push your changes.
10. Submit a pull request.

Tools to help you succeed
-------------------------

After checking out the repository, run ``script/setup`` to install dependencies. Then, run ``script/test`` to run the tests. You can also run ``script/console`` for an interactive prompt that will allow you to experiment.

Before committing code, run ``script/chores`` to check that the code conforms to the style guidelines of the project, that all of the tests are green (if you’re writing a feature; if you’re only submitting a failing test, then it does not have to pass!), and that the changes are sufficiently documented.

Releasing a new version (release maintainers only)
--------------------------------------------------

Hatch has built-in support for managing releases. Use ``hatch build`` to build the wheel and source distribution. Then, run ``tar -tvf dist/pyisemail-<version>.tar.gz`` to verify the contents of the archive. If everything looks good, publish with ``hatch publish``.
