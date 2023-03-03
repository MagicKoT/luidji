import configparser


global conf
global owners
global token
global prefix
global host
global user
global password
global database


# Подгружаем конфигурацию бота
conf = configparser.ConfigParser()
conf.read('config.ini')

# Данные подключения к MySQL
host = conf.get('database', 'host')
user = conf.get('database', 'user')
password = conf.get('database', 'password')
database = conf.get('database', 'database')

# Забираем данные ...
owners = conf.get('Settings', 'Owners')
token = conf.get('Settings', 'Token')
prefix = conf.get('Settings', 'Prefix')
