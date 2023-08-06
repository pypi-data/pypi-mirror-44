======================
chaostoolkit-openstack
======================


.. image:: https://img.shields.io/pypi/v/chaostoolkit_openstack.svg
        :target: https://pypi.python.org/pypi/chaostoolkit_openstack

.. image:: https://img.shields.io/travis/grubert65/chaostoolkit_openstack.svg
        :target: https://travis-ci.org/grubert65/chaostoolkit_openstack

.. image:: https://readthedocs.org/projects/chaostoolkit-openstack/badge/?version=latest
        :target: https://chaostoolkit-openstack.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




Chaostoolkit driver for Openstack


* Free software: BSD license


Features
--------

A minimal chaostoolkit driver for Openstack compute resources.

Secrets
-------

The driver probes/actions depends on configuration parameters stored as secrets. An
"openstack" key in the "secrets" experiment section should be present. 
The following keys should be defined in it:

* "region"
* "auth_url"
* "project_name"
* "username"
* "password"

Then in each action/probe used the "openstack" secret should be added as param.

Probes
------

The driver provides the following probes::

    # returns 1 if server name exists or 0 othewise
    check_server_name(name)


Actions
-------

The driver provides the following actions::

    # starts a server
    start_server(server_name)

    # stops a server
    stop_server(server_name)

    # suspend a server
    suspend_server(server_name)

    # resume a server
    resume_server(server_name)

    # pause a server
    pause_server(server_name)

    # unpause a server
    unpause_server(server_name)


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
