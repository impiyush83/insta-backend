from functools import wraps

from flask import current_app as app
from flask import make_response
from flask_restful import abort
from werkzeug.exceptions import HTTPException

from insta_backend.exceptions.custom_exceptions import \
    RequestValidationException, AuthenticationException, \
    ResourceAlreadyPresent, NoResultFound
from insta_backend.extensions import db


def exception_handle(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        # To be used for cerberus
        except RequestValidationException as val_err:
            app.logger.error(val_err)
            db.rollback()
            return abort(make_response(val_err.args[0], 400))
        except NoResultFound as val_err:
            app.logger.error(val_err)
            db.rollback()
            return abort(400, message=str(val_err))
        except ValueError as val_err:
            app.logger.error(val_err)
            db.rollback()
            return abort(400, message=str(val_err))
        except AuthenticationException as e:
            app.logger.error(e)
            db.rollback()
            return abort(401, message=str(e))
        except HTTPException as e:
            app.logger.error(e)
            db.rollback()
            return abort(e.code, message=e.description)
        except KeyError as key_err:
            app.logger.error(key_err)
            db.rollback()
            return abort(400, message=str(key_err))
        except IOError as io_err:
            app.logger.error()
            db.rollback()
            return abort(403, message=str(io_err))
        except ResourceAlreadyPresent as exc:
            app.logger.error(exc)
            db.rollback()
            return abort(409, message=str(exc))
        except Exception as exc:
            app.logger.error(exc)
            db.rollback()
            return abort(500, message=str(exc))
    return wrapper
