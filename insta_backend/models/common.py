from insta_backend.extensions import db


class BaseModel:
    model = None

    @classmethod
    def get_record_with_id(cls, model_id):
        return db.query(cls.model).filter(cls.model.id == model_id).first()

    @classmethod
    def get_all_records(cls, limit=100):
        query = db.query(cls.model).order_by(cls.model.id.desc())
        return query.all() if limit == 0 else query.limit(limit)

    @classmethod
    def create_record(cls, values):
        obj = cls.model(**values)
        db.add(obj)
        db.flush()
        return obj
