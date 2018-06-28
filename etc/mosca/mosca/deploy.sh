#!/bin/bash

echo 'Este vai ser o script de deploy do projeto'

#colocar aqui o código para gerar o virtualenv

#dar listen na porta no ports.conf

#recarregar configs do apache e reinicia-lo
sudo service apache2 reload && sudo service apache2 restart

#instalar automaticamente o mongodb
#wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-2.6.8.tgz
#tar -xzf mongodb-linux-x86_64-2.6.8.tgz
#mongo --port 15894 < create_users.json

#mongod.sh
#$HOME/webapps/mongo/mongodb-linux-x86_64-2.6.8/bin/mongod --auth --dbpath $HOME/webapps/mongo/data/ --port 15984  --fork --logpath $HOME/webapps/mongo/mongo_db.log

#configurar o mongod para iniciar sozinho

#Create Makefile in $HOME/webapps/
#start:
#    if ! pgrep mongod; then
#        ./<mongodb-dir-linux-version>/bin/mongod --auth --dbpath <dbpath> --port <port> --fork --logpath ./logs/mongodb.log;
#    fi
#stop:
#    pgrep mongod | xargs kill