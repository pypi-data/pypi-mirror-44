# CHANGELOG

## v0.7.2 (2019/04/11)

- bump required `sqlalchemy-unchained` version

## v0.7.1 (2019/02/26)

- bump required `sqlalchemy-unchained` version

## v0.7.0 (2018/12/09)

- do not export SessionManager or ModelManager as attributes on the extension instance

## v0.6.9 (2018/12/01)

- require sqlalchemy-unchained v0.6.9
- decouple versioning from sqlalchemy-unchained

## v0.6.8 (2018/11/07)

- add support for setting the engine-wide transaction `isolation_level` using `app.config.SQLALCHEMY_TRANSACTION_ISOLATION_LEVEL`
- require sqlalchemy-unchained v0.6.8

## v0.6.7 (2018/11/03)

- require sqlalchemy-unchained v0.6.7

## v0.6.6 (2018/10/28)

- require sqlalchemy-unchained v0.6.6

## v0.6.5 (2018/10/28)

- require sqlalchemy-unchained v0.6.5

## v0.6.4 (2018/10/28)

- require sqlalchemy-unchained v0.6.4

## v0.6.3 (2018/10/28)

- require flask-sqlalchemy 2.3.2 and sqlalchemy-unchained v0.6.3, pin versions

## v0.6.2 (2018/10/26)

- make sure to set the session factory with `SessionManager.set_session_factory`

## v0.6.1 (2018/10/23)

- update to sqlalchemy-unchained v0.6.1 (`SessionManager` bugfix)

## v0.6.0 (2018/10/23)

- **NOTE:** this package's version number is now synced with sqlalchemy-unchained
- update to sqlalchemy-unchained v0.6.0

## v0.4.1 (2018/10/20)

- require sqlalchemy-unchained >= v0.5.1

## v0.4.0 (2018/10/16)

- rename `SQLAlchemy` extension class to `SQLAlchemyUnchained`
- update to sqlalchemy-unchained v0.5.0
- indicate we are compatible with Python 3.5+

## v0.3.1 (2018/10/09)

- update import statement to reflect the model registry's renaming

## v0.1.0 (2018/09/26) - v0.3.0 (2018/10/09)

- early releases (do not use)
