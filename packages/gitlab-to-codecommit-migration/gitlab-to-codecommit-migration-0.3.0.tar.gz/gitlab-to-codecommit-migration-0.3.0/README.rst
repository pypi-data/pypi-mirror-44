==============================
gitlab-to-codecommit-migration
==============================


.. image:: https://img.shields.io/pypi/v/gitlab-to-codecommit-migration.svg
        :target: https://pypi.python.org/pypi/gitlab-to-codecommit-migration

.. image:: https://readthedocs.org/projects/gitlab-to-codecommit-migration/badge/?version=latest
        :target: https://gitlab-to-codecommit-migration.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

==================================
GitLab to AWS CodeCommit Migration
==================================

Script to migrate from GitLab to Amazon CodeCommit easily and setup your AWS environment with CodeCommit, CodePipeline and CodeDeploy as well.

Installation through pip:::

    pip install gitlab-to-codecommit-migration

Migrating one project:::

    gitlab-to-codecommit --gitlab-access-token <your-access-token> --gitlab-url https://gitlab.youdomain.com --projects namespace/project-name


Migrate all projects from a GitLab server that the secure access token gives you access to read::

    gitlab-to-codecommit --gitlab-access-token <your-access-token> --gitlab-url https://gitlab.youdomain.com --all


Or projects for a specific user or users::

    gitlab-to-codecommit --gitlab-access-token <your-access-token> --gitlab-url https://gitlab.youdomain.com --users user1 user2

Or some groups::

    gitlab-to-codecommit --gitlab-access-token <your-access-token> --gitlab-url https://gitlab.youdomain.com --groups group1 group2

And you can specify a Chime Webhook to receive notifications in a chat room as well::

    gitlab-to-codecommit --gitlab-access-token <your-access-token> --gitlab-url https://gitlab.youdomain.com --projects namespace/project-name --chime-webhook-url <chime-webhook-url>


* Free software: MIT-0 license (https://github.com/aws/mit-0)
* Documentation: https://gitlab-to-codecommit-migration.readthedocs.io.


Features
--------

Let me know :-)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
