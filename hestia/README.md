# README

Install Sass and CoffeeScript:

```
$ sudo gem install sass
$ sudo npm install -g coffee-script
```

Active a virtualenv:

```
$ virtualenv .env
$ source .env/bin/activate
```

Install packages using `pip`:

```
.env/bin/pip install -r requirements.txt
```


Initialize the app with the `invoke` task:

```
$ invoke init
```


Run the app with the `invoke` task:

```
$ invoke app
```
