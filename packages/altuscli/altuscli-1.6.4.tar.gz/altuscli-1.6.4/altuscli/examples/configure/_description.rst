Configure Altus CLI options. If this command is run with no
arguments, you will be prompted for configuration values such as your Altus
access key id and you Altus private key.  You can configure a named profile
using the ``--profile`` argument.  If your config file does not exist
(the default location is ``~/.altus/config``), the Altus CLI will create it
for you.  To keep an existing value, hit enter when prompted for the value.
When you are prompted for information, the current value will be displayed in
``[brackets]``.  If the config item has no value, it be displayed as
``[None]``.  Note that the ``configure`` command only work with values from the
config file.  It does not use any configuration values from environment
variables or the IAM role.

Note: the values you provide for the Altus Access Key ID and the Altus Private
Key will be written to the shared credentials file
(``~/.altus/credentials``).

If this command is optionally run with ``--endpoint-url`` argument,
it is persisted as part of profile configs. From there on every call using this
profile would by default use this endpoint-url setting to establish connections.


=======================
Configuration Variables
=======================

The following configuration variables are supported in the config file:

* **altus_access_key_id** - The Altus access key id part of your credentials
* **altus_private_key** - The Altus private key part of your credentials
