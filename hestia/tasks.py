from invoke import task, run

@task
def coffee():
    run('coffee -p assets/js/hestia.coffee')

@task 
def app(): 
    run('python hestia.py')
