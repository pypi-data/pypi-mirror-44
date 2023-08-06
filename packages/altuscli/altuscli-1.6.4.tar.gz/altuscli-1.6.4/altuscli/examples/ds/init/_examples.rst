Suppose you want to initialize a project::

    $ altus ds init --project jdoe/foo

      Project (jdoe/foo) initialized in current directory.

Suppose the user tries to re-init an already init'd directory::

    $ altus ds init --project "jdoe/bar"

      Project already initialized (jdoe/foo).

Suppose you want to initialize a project with a full server URL::

    $ altus ds init --project http://example.com/jdoe/bar

      Project (jdoe/bar) initialized in current directory.

