Git annex gui
=============
A small systra app for git annex assistant.

TODO
====

v0.1 - how far with qml only
----------------------------
- [x] Add icon to systray. Use the git annex icon.
- [x] Open/close the webview window by clicking the systray icon.

v0.2 - settle on language and delivery
--------------------------------------
- [x] Port c++ part to python?
- [x] Find out how to publish/deliver app.
- [x] Publish to pypi and publich gitlab/github.
- [x] Add command helper.
- [x] Remove c++ and CMake files.
- [x] Add more information to setup.py for pypi.

v0.3 - basic features
---------------------
- [x] Implement start with git-annex assistant `--autostart`
- [x] Implement stop with `git-annex assistant `--autostop`
- [ ] Implement open annex dir in file explorer. Use `xdg-open`?
  - What about BeOS style file navigation in the systray sub-menu?
- [ ] Implement start of app when desktop starts.
- [ ] Implement starting of annex daemon when app starts.
- [ ] Add more documentation to README, fix rendering in pypi, clean up todo.

v0.5 - desktop integration
--------------------------
- Forward notifications to desktop notification system?

v0.6 - in-app documentation/assistant
-------------------------------------
- allow starting the assistant wizard
- ssh-agent for pw-less login
- key handling
- remote central repo


Resources
=========

REST interface
--------------
Check the routes file in the git-annex repo (under assistant/webapp) to get an
understanding about the REST interface.

Misc
----
- recovery from corrupt repo: http://git-annex.branchable.com/tips/recovering_from_a_corrupt_git_repository/
- how to setup central repo setup
