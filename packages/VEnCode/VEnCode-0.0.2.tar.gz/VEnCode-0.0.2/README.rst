Module for VEnCode-related projects based on FANTOM5 databases
==============================================================

This module contains classes and functions that perform intersectional genetics-related operations to find VEnCodes using databases provided by the `FANTOM5 consortium`_, namely the CAGE enhancer and transcription start site (TSS) databases.

For more information on the VEnCode technology, please refer to **Macedo and Gontijo, bioRxiv 2019. DOI:**

Getting started
---------------

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

Prerequisites
^^^^^^^^^^^^^

To effectively use this module you will need Python3_ with the numpy, pandas, matplotlib and scipy libraries installed
in your machine.
Additionally, you will have to download the unannotated TSS files from `FANTOM5 consortium`_ website.

Installing
^^^^^^^^^^
1. Make sure you have the prerequisites;
2. Fork this project;
3. Put the TSS files in a folder called "Files" just outside your local forked repository.

Deployment
-----------------
Import objects from .py files (Classes.py, Plots.py) using, for example:

``from VEnCode import Classes``

to use in your own methods.
Note: You can see examples of most functions and objects being used by going to the "Scripts" folder. Old scripts can be found in somewhat obsolete files such as "main_fantom.py", even though this file still has some relevant functions for some publication panels/figures.

Contributing
------------

Please read `CONTRIBUTING.rst`_ for details on our code of conduct, and the process for submitting pull requests to us.

Versioning
----------

We use SemVer_ for versioning. For the versions available, see the `tags on this repository`_.

Authors
-------

- `André Macedo`_
- Alisson Gontijo

See also the list of contributors_ who participated in this project.

License
-------

This project is not under any free License at the moment.

Acknowledgements
----------------
- Integrative Biomedicine Laboratory @ CEDOC, NMS, Lisbon (supported by FCT: UID/Multi/04462/2019; PTDC/MED-NEU/30753/2017; and PTDC/BIA-BID/31071/2017 and FAPESP: 2016/09659-3)
- CEDOC: Chronic Diseases Research Center, Nova Medical School, Lisbon
- The MIT Portugal Program (MITEXPL/BIO/0097/2017)
- LIGA PORTUGUESA CONTRA O CANCRO (LPCC) 2017.
- FCT (IF/00022/2012, SFRH/BD/94931/2013, PTDC/BEXBCM/1370/2014)
- Prof. Dr. Ney Lemke and Ms. Benilde Pondeca for important discussions.

.. Starting hyperlink targets:

.. _FANTOM5 consortium: http://fantom.gsc.riken.jp/5/data/
.. _Python3: https://www.python.org/
.. _SemVer: https://semver.org/
.. _tags on this repository: https://github.com/AndreMacedo88/VEnCode/tags
.. _CONTRIBUTING.rst: https://github.com/AndreMacedo88/VEnCode/blob/master/CONTRIBUTING.rst
.. _contributors: https://github.com/AndreMacedo88/VEnCode/graphs/contributors
.. _André Macedo: https://github.com/AndreMacedo88
