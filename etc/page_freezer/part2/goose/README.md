## Installing

For a Debian based OS, just run the bash script present in this directory:
```
sh install.sh
```

For other OS, be sure to have installed: *redis*, *python2.7* and *virtualenv*. Both are necessary.
After installing, create a virtualenv and run the *setup.py*:
```
virtualenv ./venv
source ./venv/bin/activate
python2.7 setup.py install
```


## Running

This package runs on top of Huey. After installed the package and activated the virtualenv, do in one terminal and it will start the message queue and load the tasks:
```
redis-cli FLUSHALL; huey_consumer.py main.hueymq -w 16 -q
```
Note: this line runs it with 16 thread based workers, if you want. Just increase or decrease to as many as you like. The *redis-cli* call is to clear redis contents and avoid any problem with some "leftovers".

With Huey running, just run the following line in another terminal to provide urls to the tasks:
```
python goose/main.py
```

It will start to show output on the message queue screen and output the required data to the file *logs.log*.


## Testing

The tests are all done on top of *py.test*.
To run them, just do:
```
python setup.py test
```
