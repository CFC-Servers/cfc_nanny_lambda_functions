from json import dumps

class ResponseBuilder:
    def build(self):
        body = {}
        content = self.content
        errors = self.errors

        if content:
            if type(content) is dict:
                for key, value in content.items():
                    body[key] = value
            else:
                body["response"] = content

        if errors:
            if type(errors) is not list:
                errors = [errors]

            body["errors"] = errors

        body = dumps(body)

        return {
            "statusCode": self.status,
            "body": body,
            "headers": self.headers
        }

class Response:
    def __new__(cls, content=None, errors=None, status=200, cache_lifetime=None):
        response = ResponseBuilder()
        response.status = status
        response.content = content
        response.errors = errors
        response.headers = { "Cache-Control": "no-store" }

        if cache_lifetime:
            response.headers["Cache-Control"] = (
                "public,"
                "max-age 0,"
               f"s-maxage {cache_lifetime},"
                "proxy-revalidate"
            )

        return response.build()

