Suppose you want to take the snapshot of the current initialized workspace::

    $ altus ds snapshot [--comment "Added new files"]

    Counting objects: 4, done.
    Compressing objects:  50% (1/2)
    Compressing objects: 100% (2/2)
    Compressing objects: 100% (2/2), done.
    Writing objects:  25% (1/4)
    Writing objects:  50% (2/4)
    Writing objects:  75% (3/4)
    Writing objects: 100% (4/4)
    Writing objects: 100% (4/4), 401 bytes | 0 bytes/s, done.

    Created snapshot ID:(7cebab5f5fa304440e625ecb059bf08820dcc517)

A project must be initialized before it can be snapshotted::

    $ altus ds snapshot

    Project has not been initialized.
    Run `altus ds init` to initialize workspace.

