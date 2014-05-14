import os, shutil
from invoke import task, run

@task
def coffee():
    run('coffee -p assets/js/hestia.coffee')

@task 
def app(): 
    run('python hestia.py')

@task
def init():
    os.mkdir('logs')
    shutil.copy('config.example.yaml', 'config.yaml')
