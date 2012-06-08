GitHub Service Hook Plugin for Trac
===================================

Adds your git commit messages as comments to your trac tickets.
If a commit pushed to your github project contains a trac ticket number like
`#123` anywhere in the commit message, this trac plugin will add your commit
message as a comment to your trac ticket, like this:

    Sean Hammond c814c9f5c9b94389bbc169d305f58f779f232d52

    Lorem Ipsum, see ticket #123

    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor
    incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
    nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
    Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
    fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
    culpa qui officia deserunt mollit anim id est laborum.

The SHA-1 of the commit message will be hyperlinked to the commit's page on
github.

The code is based on
[github-trac](https://github.com/davglass/github-trac), but:

- It adds your git commit messages to your trac tickets, I don't think
  github-trac does that.
- It will find any use of `#123` in a commit message, not just commands like `see
  #123`, `closes #123`, etc. It will even find things like `(#123)` or `[#123]`.
- It doesn't automatically close trac tickets if you say `closes #123` etc. in
  your git commits, we didn't want that (this could be added as an optional
  behaviour).
- It doesn't do trac source code browser redirects.
- It's much simpler than github-trac.

## Install

1. Install the plugin into your trac project's plugins dir:

       cd /path/to/your/trac/project/plugins
       git clone git://github.com/seanh/githubservicehook.git
       cd githubservicehook
       python setup.py install

2. Enable the github service hook.  Go to the admin panel of your project on
github and enable the trac service hook. Set URL to your trac instance's URL,
and set Token to whatever you like.

3. Enable the plugin. Edit your trac.ini file and add:

       [components]
       githubservicehook.* = enabled
       
       [githubservicehook]
       token = YOUR_TOKEN

where YOUR_TOKEN is the same token that you set in your github project.

4. Finally, restart the web server that hosts your trac instance.
