Suppose you want to run an experiment in an uninitialized workspace::

    $ altus ds run --script test.py --project jdoe/foo

    ----------------------------------------------------------------------------
    |                                    run                                   |
    +-----------+--------------------------------------------------------------+
    |  buildId  |  0f953a8c-2b02-4429-a11f-2dfe5a35f880                        |
    |  createdAt|  2018-03-29 02:17:24.025000+00:00                            |
    |  id       |  1                                                           |
    |  projectId|  1                                                           |
    |  webLink  |  http://cdsw.foo.com/jdoe/foo/runs/1                         |
    +-----------+--------------------------------------------------------------+

Suppose you want to run an experiment by passing a snapshot id in an uninitialized workspace::

    $ altus ds run --script test.py --project jdoe/foo --snapshot-id <ID>

    ----------------------------------------------------------------------------
    |                                    run                                   |
    +-----------+--------------------------------------------------------------+
    |  buildId  |  0f953a8c-2b02-4429-a11f-2dfe5a35f881                        |
    |  createdAt|  2018-03-29 02:17:25.025000+00:00                            |
    |  id       |  2                                                           |
    |  projectId|  1                                                           |
    |  webLink  |  http://cdsw.foo.com/jdoe/foo/runs/2                         |
    +-----------+--------------------------------------------------------------+

Suppose you want to run an experiment by uploading current working directory contents in an initialized workspace::

    $ altus ds run --script test.py

    Counting objects: 2, done.
    Compressing objects:  50% (1/2)
    Compressing objects: 100% (2/2)
    Compressing objects: 100% (2/2), done.
    Writing objects:  50% (1/2)
    Writing objects: 100% (2/2)
    Writing objects: 100% (2/2), 242 bytes | 0 bytes/s, done.

    Created snapshot ID:(301698d58775933d19d474564a299d75f86eeba1)

    ----------------------------------------------------------------------------
    |                                    run                                   |
    +-----------+--------------------------------------------------------------+
    |  buildId  |  0f953a8c-2b02-4429-a11f-2dfe5a35f882                        |
    |  createdAt|  2018-03-29 02:17:26.026000+00:00                            |
    |  id       |  3                                                           |
    |  projectId|  1                                                           |
    |  webLink  |  http://cdsw.foo.com/jdoe/foo/runs/3                         |
    +-----------+--------------------------------------------------------------+


Suppose you want to run an experiment by specifying the snapshot id in an initialized workspace::

    $ altus ds run --script test.py --snapshot-id <ID>

    ----------------------------------------------------------------------------
    |                                    run                                   |
    +-----------+--------------------------------------------------------------+
    |  buildId  |  0f953a8c-2b02-4429-a11f-2dfe5a35f883                        |
    |  createdAt|  2018-03-29 02:17:26.027000+00:00                            |
    |  id       |  4                                                           |
    |  projectId|  1                                                           |
    |  webLink  |  http://cdsw.foo.com/jdoe/foo/runs/4                         |
    +-----------+--------------------------------------------------------------+

