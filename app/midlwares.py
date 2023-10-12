import time
import datetime
from fastapi import Response
from app.controllers.elasticsearch import ElasticsearchController
from app.constants import ELASTIC_INDEX_LOG


async def read_stats(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk

    time_now = datetime.datetime.now()
    stats = {
        '@timestamp': time_now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        'process-time': process_time,
        'request': request.url._url,
        'request-type': request.method,
        # 'response': response_body.decode(),
        'status': response.status_code,
    }
    if response.status_code != 307:
        await ElasticsearchController().create_document(index=ELASTIC_INDEX_LOG, data=stats)

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )
