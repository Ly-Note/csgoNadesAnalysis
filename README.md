# csgoNadesAnalysis
csgo Nades Analysis
main update
py manage.py startapp polls 创建分支
py manage.py runserver

py manage.py startapp xxxxx 创建分支
py manage.py runserver


编辑 models.py 文件，改变模型。
运行 python manage.py makemigrations matches xxxx为模型的改变生成迁移文件。
运行 python manage.py migrate 来应用数据库迁移。
py manage.py test xxxxx    测试

python manage.py createsuperuser 创建一个能登录管理页面的用户
python manage.py flush --noinput