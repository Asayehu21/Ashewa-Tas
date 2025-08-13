class SecondaryRouter:
    """
    Routes DB operations for import API models to 'secondary'
    """
    def db_for_read(self, model, **hints):
        if getattr(model._meta, 'app_label', None) == 'secondary':
            return 'secondary'
        return None

    def db_for_write(self, model, **hints):
        if getattr(model._meta, 'app_label', None) == 'secondary':
            return 'secondary'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # allow relations within same db
        db_list = ('default', 'secondary')
        if obj1._state.db in db_list and obj2._state.db in db_list:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'secondary':
            return db == 'secondary'
        return db == 'default'
