This is a simple program to add exceptions in a certain simple VPN setup. Since this setup is popular, I figured I'd publish it. The Python file is intended to be executed as root after openvpn -- it is ideal to run it as a hook for openvpn. It can be re-run without leaving garbage entries in your routing table or firewall -- designed to clean up after itself.

It could also be made a systemd service if you wanted to keep it seperate or if you had limited permissions in your openvpn scope, I suppose.

All you have to do is add the domains you want to be exceptions under /etc/vde.conf, and it should do the rest for you!

TODO: clean up makefile with fancy formatting and examples and whatever else.
