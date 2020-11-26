from json import dumps

class Response:
    def __new__(self, content=None, errors=None, status=200, cache_lifetime=None):
        self.status = status
        self.content = content
        self.errors = errors
        self.headers = { "Cache-Control": "no-store" }

        if cache_lifetime:
            self.headers["Cache-Control"] = (
                "public,"
                "max-age 0,"
                "s-maxage {},".format(cache_lifetime)
                "proxy-revalidate"
            )

        return self.build()

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
