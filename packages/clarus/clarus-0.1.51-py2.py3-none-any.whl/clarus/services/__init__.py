from __future__ import print_function
import clarus
import clarus.api
from clarus.models import ApiResponse, ApiError
from clarus.multipart import PartWrapper
from requests_toolbelt import MultipartDecoder


def api_request(serviceCategory, service, output=None, responses=None, **params):
    httpresp = clarus.api.request(serviceCategory, service, output, **params);
    if (httpresp.status_code != 200):
        raise ApiError(httpresp)
    else:
        content_type = httpresp.headers.get('content-type', None)

        if (content_type is not None and content_type.startswith('multipart/')):
            decoder = MultipartDecoder.from_response(httpresp)

            rs=[ApiResponse(PartWrapper(part, httpresp)) for part in decoder.parts]

            if (responses is not None):
                for r in rs: 
                    responses.append(r)

                return rs[0]
            else:
                return ApiResponse(httpresp);
