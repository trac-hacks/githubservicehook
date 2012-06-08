GitHub Service Hook Plugin for Trac
===================================

Reference trac tickets in your git commits, e.g. #123, and have your
commit messages added as comments to your trac tickets.

This is a trac plugin that listens to github's trac service hook, parses
the data from github, and adds you git commit messages as comments to
the trac tickets that they reference.

The code is based on
[github-trac](https://github.com/davglass/github-trac), but:

- It adds your git commit messages to your trac tickets, I don't think
  github-trac does that
- It doesn't automatically close trac tickets if you say "closes #123" etc. in
  your git commits, we didn't want that (this could be added as an optional
  behaviour)
- It doesn't do source code browser redirects
- It's much simpler than github-trac

## Install

    cd /path/to/your/trac/project/plugins
    git clone git://github.com/seanh/githubservicehook.git
    cd githubservicehook
    python setup.py install

Go to the admin panel of your project on github and enable the trac service
hook. Set URL to your trac instance's URL, and set Token to whatever you like.

Edit your trac.ini file and add:

    [components]
    githubservice.* = enabled

    [githubservicehook]
    token = YOUR_TOKEN

where YOUR_TOKEN is the same token that you set in your github project.

Finally, restart the web server that hosts your trac instance.
