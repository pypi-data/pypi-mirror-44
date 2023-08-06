phovea_security_flask [![Phovea][phovea-image]][phovea-url] [![NPM version][npm-image]][npm-url] [![Build Status][travis-image]][travis-url] [![Dependency Status][daviddm-image]][daviddm-url]
=====================

Security manager implementation based on [Flask-Login](https://flask-login.readthedocs.io/en/latest/). Additionally, a login module is provided that can be used at client-side.

Installation
------------

```
git clone https://github.com/phovea/phovea_security_flask.git
cd phovea_security_flask
npm install
```

Testing
-------

```
npm test
```

Building
--------

```
npm run build
```

Add new users
-------

### Config File
New users are added to `phovea_security_flask/config.json`.

The python script `encryptor.py` hashes a given password and prints password, salt, and hashed password.

### Environment Variables
Alternatively, you can provide users via environment variables:
The `UserStore` class in `phovea_security_flask/dummy_store.py` reads all environment variables starting with `PHOVEA_USER_` and uses the remainder of the enviroment variable key as username. The environment variable's key has to contain: `SALT;HASHED_PW;ROLE1` (multiple roles can be added by seperating them with a semicolon), e.g.:
```
export PHOVEA_USER_bruce.banner="08c52b567cb947c98be6de6e9ad3919f;2c946ca1b8574d506ee5e7b3b22e350bc8c93b9df647d17e4429e727529c63a62d1fb274ca5a7499bd33c0844e437631728ee9fcba14b41204f21ec8cda523f7;avenger;scientist
```

Defines the following user:
* Username: `bruce.banner`
* Salt: `08c52b567cb947c98be6de6e9ad3919f`
* Hashed password: `2c946ca1b8574d506ee5e7b3b22e350bc8c93b9df647d17e4429e727529c63a62d1fb274ca5a7499bd33c0844e437631728ee9fcba14b41204f21ec8cda523f7`
* Roles: `avenger, scientist`

**NOTE:** User credentials defined as environment variables override all users defined in the `config.json`. This behaviour can be used to define development users inside the `config.json`, and provide users for production via environment variables when deployed.


***

<a href="https://caleydo.org"><img src="http://caleydo.org/assets/images/logos/caleydo.svg" align="left" width="200px" hspace="10" vspace="6"></a>
This repository is part of **[Phovea](http://phovea.caleydo.org/)**, a platform for developing web-based visualization applications. For tutorials, API docs, and more information about the build and deployment process, see the [documentation page](http://phovea.caleydo.org).


[phovea-image]: https://img.shields.io/badge/Phovea-Client%20Plugin-F47D20.svg
[phovea-url]: https://phovea.caleydo.org
[npm-image]: https://badge.fury.io/js/phovea_security_flask.svg
[npm-url]: https://npmjs.org/package/phovea_security_flask
[travis-image]: https://travis-ci.org/phovea/phovea_security_flask.svg?branch=master
[travis-url]: https://travis-ci.org/phovea/phovea_security_flask
[daviddm-image]: https://david-dm.org/phovea/phovea_security_flask/status.svg
[daviddm-url]: https://david-dm.org/phovea/phovea_security_flask


