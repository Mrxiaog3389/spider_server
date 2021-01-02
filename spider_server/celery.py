import os
import django
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spider_server.settings')
django.setup()

app = Celery('spider_server')
app.config_from_object('django.conf:settings')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
# 获取当前文件夹名，即为该Django的项目名
# project_name = os.path.split(os.path.abspath('.'))[-1]
# project_settings = '%s.settings' % project_name
#
# # 设置环境变量 主要可用于在定时任务 或者其他任务中操作数据库
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)
#
# # 实例化Celery
# app = Celery(project_name)
#
# # 使用anync_task.celery_config
# app.config_from_object(spider_one.celery_config)
#
# # Celery加载所有注册的应用
# app.autodiscover_tasks(lambda: spider_one.INSTALLED_APPS)
