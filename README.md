用于介绍项目信息
问题1、python manage.py dbshell
提示：CommandError: You appear not to have the 'sqlite3' program installed or on your path
解决：sudo apt-get install sqlite3 libsqlite3-dev

2.认识：model层中增加一个objects属性，来提供数据操作的接口。