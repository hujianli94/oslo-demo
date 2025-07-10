from oslo_context import context as os_context
import uuid


def create_context():
    return os_context.RequestContext(
        user_id='6ce90b4d',
        project_id='d6134462',
        domain_id='a6b9360e',
        request_id=f'req-{uuid.uuid4()}'
    )
