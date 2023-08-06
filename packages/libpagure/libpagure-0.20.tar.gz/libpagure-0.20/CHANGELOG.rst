CHANGELOG
=========

0.20 (2019-04-10)
-----------------
- fix flake8 error
- pass "errors" to exc in != 200
- Add log_debug
- add create_pr function
- Use the requests sessions to retry failed connection
- Add an user guide documentation
- Add .tox .venv and .vscode to gitignore
- Provide more information about contribution in the Readme
- Use black to format the code base
- README: "warp" -> "wrapper"
- Added 4 API methods and their test cases for getting more stats of pagure users - user_activity_stats - user_activity_stats_by_date - list_pull_requests - list_prs_actionabl
e_by_user
- Beginning of unit test.
- Update list_issues to newest API
- Update create_issue with the latest API
- new_project: create_readme is never None
- new_project: Enable creating private repos
- Support namespaces
- Add support for listing repository branches
- list_projects: Add missing filter options

0.10 (2017-09-06)
-----------------

- Add tox to run tests - #26 (cqi)
- Just log message returned from pagure - #22 #23 (cqi)
