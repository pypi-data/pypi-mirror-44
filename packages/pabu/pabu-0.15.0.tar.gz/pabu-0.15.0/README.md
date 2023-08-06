About
-----

time tracker app

Dev
---

* use virtualenv!
* install: `pip install -e .`
* start server: `./run-dev-server`
* dev build bundle.js: `npm start`


Deploy
------
```
$ pip install -e .[deploy]
$ git tag -a v1.42.0 -m 'v1.42.0'
$ ./generate-changelog
$ npm run-script build
$ twine upload
$ git push --tags
```
