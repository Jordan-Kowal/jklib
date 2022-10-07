# Built-in
import urllib
import zipfile
from io import BytesIO

# Django
from django.core.files.storage import Storage
from django.http import HttpResponse, StreamingHttpResponse


def download_file(path: str, storage: Storage) -> StreamingHttpResponse:
    """"""
    filename = urllib.parse.urlparse(path).path.split("/").pop()
    response = StreamingHttpResponse(streaming_content=storage.open(path))
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def download_files_as_zip(
    paths: str, output_filename: str, storage: Storage
) -> HttpResponse:
    content = BytesIO()
    with zipfile.ZipFile(content, "w") as zf:
        for path in paths:
            filename = urllib.parse.urlparse(path).path.split("/").pop()
            zf.writestr(filename, storage.open(path).read())
    response = HttpResponse(content.getvalue())
    response["Content-Disposition"] = f'attachment; filename="{output_filename}"'
    return response
