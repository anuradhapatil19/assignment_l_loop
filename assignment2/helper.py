def serialize_task(task):
    task.__dict__.pop('_sa_instance_state')
    return task.__dict__
