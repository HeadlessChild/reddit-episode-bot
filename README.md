# reddit-episode-bot
This bot will look for comments referencing episodes for a tv show. If it finds one it will respond with some scaled-down information about that particular episode.

## Install
Install the following Debian packages:
  ```
  sudo apt-get install python-mysqldb python-configparser python-pip
  ```

Install the following pypi packages:
  ```
  sudo pip install pyopenssl praw tvdb_api
  ```
  
## Database
You need to have a SQL database on your host, I use MariaDB. To install MariaDB do the following:  
  ```
  sudo apt-get install mariadb-server-10.0 mariadb-client-10.0 mariadb-server-core-10.0  mariadb-client-core-10.0 maridb-common
  ```
  
Enable and start mysql (MariaDB) service: 
  ```
  sudo systemctl enable mysql.service
  sudo systemctl start mysql.service
  ```

NOTE: Enable will start MariaDB at boot.

## Config
Create a ```.reddit-bot-episode.conf``` at your home directory (/home/$(USER)/.reddit-episode-bot.conf).

Example config file:
```
[Show]
Tvshow = Seinfeld

[Reddit]
Username = SeinfeldEpisodeBot
Password = password

[MySQL]
Username = root
password = root
```

## Run the bot
To run the bot you simply run the following command:
```
python reddit-episode-bot.py
```

# Docker
You can run this bot inside a Docker container. You need a mysql database on the host and mount the socket to the container.

## Run Docker container
You have to mount the mysql socket inside the container, the following command will do:

    docker run \
              -d \
              -v $HOME/.reddit-episode-bot.conf:/root/.reddit-episode-bot.conf \ #You have to create config file first
              -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock \  #Might have to change to suit your system
              --name reddit-episode-bot \
              markuslindberg/reddit-episode-bot

## Systemd service file for Docker conatiner
You can use this systemd service file for handling start/stop of the container. You can use the following:

    [Unit]
    Description="Reddit Episode Bot"
    After=docker.service
    Requires=docker.service
    
    [Service]
    TimeoutStartSec=0
    ExecStartPre=-/usr/bin/docker kill reddit-episode-bot
    ExecStartPre=-/usr/bin/docker rm reddit-episode-bot
    ExecStartPre=/usr/bin/docker pull markuslindberg/reddit-episode-bot
    ExecStart=/usr/bin/docker run -v <path-to>/.reddit-episode-bot.conf:/root/.reddit-episode-bot.conf -v /var/run/mysqld/mysqld.sock:/var/run/mysqld/mysqld.sock --name reddit-episode-bot markuslindberg/reddit-episode-bot
    ExecStop=-/usr/bin/docker stop reddit-episode-bot

    [Install]
    WantedBy=multi-user.target
    
Create this file in ```/lib/systemd/system/reddit-episode-bot.service```

Then you can enable the service and start it.

  ```
  sudo systemctl enable reddit-episode-bot.service
  sudo systemctl start reddit-episode-bot.service
  ```
NOTE: Enable will start the container at boot.
