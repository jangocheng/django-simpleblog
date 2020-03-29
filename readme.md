一个用 Django 搭建的个人博客网站后端, 博客效果: http://lowbeeland.com
前端Vue写的太屎, 还在整理当中, 需要的可以加我微信获取, 联系方式在最下方

# 环境依赖

<p><a href="https://www.python.org/downloads/release/python-364/"><img alt="Python" src="https://img.shields.io/badge/python-3.6.4-brightgreen.svg?style=flat-square"></a>
<a href="https://docs.djangoproject.com/zh-hans/2.0/"><img alt="Django" src="https://img.shields.io/badge/django-2.0.7-blue.svg?style=flat-square"></a>

* 使用 Python 3.6 + Django 2.0 进行搭建
* 后台数据库使用 MySQL, 缓存数据库使用 Redis
* 使用 Django REST framework 开发的符合 RESTful 规范的 API 接口
* 使用 Celery 执行周期任务同步后台数据库和缓存数据库
* 使用 SimpleUI 作为网站后台管理系统
* 调用腾讯云接口实现短信验证码注册/登录
* 网站其他依赖请查看源码 requirements.txt 文件

# 使用说明

请确保你的PC拥有 Python 3.6+/MySQL/Redis 环境

* 安装依赖

```
pip install -r requirements.txt
```

* 修改`simpleblog/settings/dev.py` 中的数据库配置 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'simpleblog',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
```

* 创建数据库 (mysql数据库中执行)

```
create database simpleblog charset=utf8;
```

* 进行数据库迁移 (项目目录下执行)

```
python manage.py makemigrations
python manage.py migrate
```

* 运行 redis

```
redis-server --service-start
```

* 运行 celery (项目目录下执行)

```python
celery worker -A celery_task -l info -P eventlet
celery beat -A celery_task -l info 
```

* 运行项目 (项目目录下执行)

```
python manage.py runserver
```

# 注意

由于用户模块调用了腾讯云短信验证码接口, 为了保证用户模块的正常运行, 你还需要在[腾讯云]( https://console.cloud.tencent.com/smsv2)申请接口所需的AppID, AppKey, 短信模板ID和短信签名, 并在`simpleblog/libs/tx_sms/settings.py`中完成如下配置

```python
# 短信应用 SDK AppID
APP_ID = 123456

# 短信应用 SDK AppKey
APP_KEY = '******'

# 短信模板(模块ID)
TEMPLATE_ID = 123456

# 短信签名(签名内容)
SMS_SIGN = '洛碧兰德'
```

# 联系方式

任何项目相关问题和建议你都可以和我联系, 联系方式如下

* 邮箱: `lowbeeland@163.com`
* 微信: 扫描下方二维码加我微信

![](https://lowbeeland.oss-cn-shanghai.aliyuncs.com/wechat.jpg )





