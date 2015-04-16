def get_or_create(session, model, **kwargs):
    """
    Creates an object or returns the object if exists
    credit to Kevin @ StackOverflow
    from: http://stackoverflow.com/questions/2546207/does-sqlalchemy-have-an-equivalent-of-djangos-get-or-create
    """

    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        return instance
