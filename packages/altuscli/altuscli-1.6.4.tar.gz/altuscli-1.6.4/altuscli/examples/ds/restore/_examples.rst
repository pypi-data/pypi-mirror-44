Suppose you want to restore a snapshot in the current initialized workspace::

    $ altus ds restore --snapshot-id 7cebab5f5fa304440e625ecb059bf08820dcc517

    Restored snapshot ID:(7cebab5f5fa304440e625ecb059bf08820dcc517)

A project must be initialized before it can be restored::

    $ altus ds restore --snapshot-id 7cebab5f5fa304440e625ecb059bf08820dcc517

    Project has not been initialized.
    Run `altus ds init` to initialize workspace.

