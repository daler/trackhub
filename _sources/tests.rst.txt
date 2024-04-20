
.. _tests:

Testing infrastructure
======================
Tests are run on GitHub Actions, configured in ``.github/workflows/main.yml``.

In addition to unit tests, now any code in the documentation that shows how to
build example track hubs is handled like this:

- extract code from documentation (see ``ci/example_hubs.tsv`` for the list of
  files from which code is extracted)
- execute code to build track hub (see ``ci//build_examples.py``)
- upload code and built track hub (and data, if relevant) to the `trackhub-demo
  <https://github.com/daler/trackhub-demo>`_ repository
- run ``hubCheck`` on the just-uploaded hubs (see ``ci/check_hubs.py``)

The just-built track hubs are then live, and linked to from within the
documentation.
