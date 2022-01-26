# kerberi
Get all kerberi from lists, recursively searching. Uses blanche.

To get a list of most undergrads at MIT, try

```
./kerberi.sh nh-forum ec-discuss bc-talk next-forum random-hall-talk hackmit-hackers hackmit-exec hkn-eligibles-fa21 hkn-eligibles-fa20 mec-all uiux-members sipb-members esp
```

(must be run on Athena)

An alternative way to get kerberi is to list the directories under `/afs/athena.mit.edu/user`, but this includes everyone, not only undergrads. We kind of only want undergrads and CSAIL grad students.
