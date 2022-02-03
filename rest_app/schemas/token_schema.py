from rest_app import ma


class TokenSchema(ma.Schema):
    class Meta:
        ordered = True

    access_token = ma.String(required=True)
