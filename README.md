# book-template



# build
```
$ pip install -U pipenv
$ pipenv shell
$ sudo bash ./install-tex.sh
$ make latexpdfja
$ cp build/latex/gps-ntp.pdf .
```

## Docker

```bash
docker run -it -v `pwd`:/work -w /work misodengaku/tex make latexpdfja
```
