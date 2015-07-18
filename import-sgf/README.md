Download & unarchive SGF files

```
cd sgf
wget -r -l1 -H -t1 -nd -N -A.bz2 -erobots=off http://u-go.net/gamerecords/
for f in *.tar.bz2; do tar xf $f; done
rm -f *.tar.bz2
```
