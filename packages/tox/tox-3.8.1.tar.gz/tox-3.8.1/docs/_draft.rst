*Changes in master, but not released yet are under the draft section*.

vDRAFT (2019-03-28)
-------------------


Bugfixes
^^^^^^^^

- The ``-eALL`` command line argument now expands the ``envlist`` key and includes all its environment.
  `#1155 <https://github.com/tox-dev/tox/issues/1155>`_
- Isolated build environment dependency overrides were not taken in consideration (and such it inherited the deps
  from the testenv section) - by :user:`gaborbernat`
  `#1207 <https://github.com/tox-dev/tox/issues/1207>`_
- Set ``setup.cfg`` encoding to UTF-8 as it contains Unicode characters.
  `#1212 <https://github.com/tox-dev/tox/issues/1212>`_
- Fix tox CI, better error reporting when locating via the py fails - by :user:`gaborbernat`
  `#1215 <https://github.com/tox-dev/tox/issues/1215>`_

