.. image:: https://gitlab.com/hmajid2301/gitlab-auto-mr/badges/master/pipeline.svg

.. image:: https://img.shields.io/pypi/l/gitlab-auto-mr.svg

.. image:: https://img.shields.io/pypi/v/gitlab-auto-mr.svg

GitLab Auto MR
==============

This is a simple Python script that allows you create MR in GitLab automatically. It is intended to be used in CI/CD
as a Docker image. However you can use it as a separate Python library if you would like.
An example CI using this can be found `here <https://gitlab.com/hmajid2301/stegappasaurus/blob/master/.gitlab-ci.yml>`_.

It is based on the script and idea of `Riccardo Padovani <https://rpadovani.com>`_,
which he introduced with his blog post
`How to automatically create new MR on Gitlab with Gitlab CI <https://rpadovani.com/open-mr-gitlab-ci>`_.

This package was intended to be used by GitLab CI hence using environments provided by the GitLab CI. You can however
use it as a CLI tool if you would like.

Usage
-----

First you need to create a personal access token,
`more information here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
With the scope ``api``, so it can create the MR using your API.

.. code-block::

    pip install gitlab-auto-mr
    gitlab_auto_mr --help

    Usage: gitlab_auto_mr [OPTIONS]

Options:
  --private-token TEXT      Private GITLAB token, used to authenticate when
                            calling the MR API.  [required]
  --source-branch TEXT      The source branch to merge into.  [required]
  --project-id INTEGER      The project ID on GitLab to create the MR for.
                            [required]
  --project-url TEXT        The project URL on GitLab to create the MR for.
                            [required]
  --user-id INTEGER         The GitLab user ID to assign the created MR to.
                            [required]
  --target-branch TEXT      The target branch to merge onto.
  --commit-prefix TEXT      Prefix for the MR title i.e. WIP.
  --remove-branch BOOLEAN   Set to True if you want the source branch to be
                            removed after MR.
  --squash-commits BOOLEAN  Set to True if you want commits to be squashed.
  --description TEXT        Description in the MR.
  --use-issue-name BOOLEAN  If set to True will use information from issue in
                            branch name, must be in the form #issue-number,
                            i.e feature/#6.
  --help                    Show this message and exit.

.. code-block::

    gitlab_auto_mr --private-token $(private_token) --source-branch feature/test --project-id 5 \
                    --project-url https://gitlab.com/hmajid2301/stegappasaurus --user-id 5

GitLab CI
*********

``GITLAB_PRIVATE_TOKEN`` Set a secret variable in your GitLab project with your private token. Name it
GITLAB_PRIVATE_TOKEN (``CI/CD > Environment Variables``). This is necessary to raise the Merge Request on your behalf.
More information `click here <https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html>`_.
An example CI using this can be `found here <https://gitlab.com/hmajid2301/stegappasaurus/blob/master/.gitlab-ci.yml>`_.

Add the following to your ``.gitlab-ci.yml`` file:

.. code-block::

    stages:
      - open

    open_merge_request:
      image: registry.gitlab.com/hmajid2301/gitlab-auto-mr
      before_script: [] # We do not need any setup work, let's remove the global one (if any)
      variables:
        GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
      stage: open
      only:
        - /^feature\/*/ # We have a very strict naming convention
      script:
        - gitlab_auto_mr

You can set extra variables like so.

.. code-block::

    variables:
      GIT_STRATEGY: none # We do not need a clone of the GIT repository to create a Merge Request
      TARGET_BRANCH: master # Target branch for MR

- COMMIT PREFIX: Prefix for the MR i.e. WIP
- REMOVE_BRANCH_AFTER_MERGE: Will delete branch after merge
- SQUASH: Will squash commits after merge
- AUTO_MERGE: Will auto merge request after being reviewed and CI passes
- TARGET_BRANCH: The target branch for the MR
- DESCRIPTION: Description of the MR
- USE_ISSUE_NAME: If set to True will use information from issue in branch name, must be in the form #issue-number, i.e feature/#6.

Authors
=======

- Extra features: `Allsimon <https://gitlab.com/Allsimon/gitlab-auto-merge-request>`_
- Forked from: `Tobias L. Maier <https://gitlab.com/tmaier/gitlab-auto-merge-request>`_
- Script and idea: `Riccardo Padovani <https://rpadovani.com>`_
