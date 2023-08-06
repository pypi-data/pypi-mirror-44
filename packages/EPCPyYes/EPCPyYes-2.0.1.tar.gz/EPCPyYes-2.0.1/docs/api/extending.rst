Extending The Templates
=======================

The templates in the EPCPyYes/templates/epcis directory are all Jinja2
templates. If you'd like to inherit and extend them, the EPCPyYes module
exposes the path to these templates via the `EPCPyYes.TEMPLATES_PATH`
property.  This will return the path to the templates directory wherever
the EPCPyYes module was installed.

For example, to load the EPCPyYes modules into a Jinja2 environment, you can
use the FileSystemLoader as below.

.. code-block:: python

    import EPCPyYes
    from jinja2.loaders import FileSystemLoader
    loader = FileSystemLoader(EPCPyYes.TEMPLATES_PATH)

