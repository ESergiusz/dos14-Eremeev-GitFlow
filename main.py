import json
import yaml
from flask import Flask, jsonify, request

app_flask = Flask(__name__)
roles = {}
organisations = []
users = []
apps = []


class Permissions:
    def __init__(self, create=False, read=False, update=False, delete=False):
        self._create = create
        self._read = read
        self._update = update
        self._delete = delete

    def to_dict(self):
        return {
            "create": self._create,
            "read": self._read,
            "update": self._update,
            "delete": self._delete,
        }

    @property
    def create(self):
        return self._create

    @property
    def read(self):
        return self._read

    @property
    def update(self):
        return self._update

    @property
    def delete(self):
        return self._delete


class Role:
    def __init__(self, name, permissions):
        self._name = name
        self._permissions = permissions
        self._role = {k: Permissions(**v) for k, v in permissions.items()}

    def to_dict(self):
        perm = {}
        for key, value in self._role.items():
            perm[key] = value.to_dict()
        return {"name": self._name, "permissions": perm}

    @property
    def name(self):
        return self._name

    @property
    def permissions(self):
        return self._permissions

    def __getitem__(self, key):
        return self._role[key]


class Client:
    def __init__(self, client_id, role):
        self._client_id = client_id
        self._role = role

    @property
    def client_id(self):
        return self._client_id

    @property
    def role(self):
        return self._role


class User(Client):
    def __init__(
        self, client_id, first_name, last_name, fathers_name, date_of_birth, role
    ):
        super().__init__(client_id, role)
        self._first_name = first_name
        self._last_name = last_name
        self._fathers_name = fathers_name
        self._date_of_birth = date_of_birth

    def to_dict(self):
        return {
            "client_id": self._client_id,
            "first_name": self._first_name,
            "role": self._role.to_dict(),
            "last_name": self._last_name,
            "fathers_name": self._fathers_name,
            "date_of_birth": self._date_of_birth,
        }

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def fathers_name(self):
        return self._fathers_name

    @property
    def date_of_birth(self):
        return self._date_of_birth

    @property
    def age(birth, year=2023):
        result = year - birth
        return result


class Organisation(Client):
    def __init__(self, client_id, role, creation_date, unp, name):
        super().__init__(client_id, role)
        self._creation_date = creation_date
        self._unp = unp
        self._name = name

    def to_dict(self):
        return {
            "client_id": self._client_id,
            "role": self._role.to_dict(),
            "creation_date": self._creation_date,
            "unp": self._unp,
            "name": self._name,
        }

    @property
    def creation_date(self):
        return self._creation_date

    @property
    def unp(self):
        return self._unp

    @property
    def name(self):
        return self._name


class App(Client):
    def __init__(self, client_id, name, role):
        super().__init__(client_id, role)
        self._name = name

    def to_dict(self):
        fields = {
            "client_id": self._client_id,
            "name": self._name,
            "role": self._role.to_dict(),
        }
        return fields

    @property
    def name(self):
        return self._name


with open("roles.yaml", "r", encoding="utf8") as yamlfile:
    roles_data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    for role_name, role_data in roles_data.items():
        roles[role_name] = Role(role_name, role_data)

with open("users.json", "r", encoding="utf8") as filejson:
    users_data = json.loads(filejson.read())["Users"]
    for user_data in users_data:
        user = User(
            int(user_data["client_id"]),
            user_data["first_name"],
            user_data["last_name"],
            user_data["fathers_name"],
            user_data["date_of_birth"],
            roles[user_data["role"]],
        )
        users.append(user)

with open("users.json", "r", encoding="utf8") as filejson:
    organisations_data = json.loads(filejson.read())["Organisations"]
    for org_data in organisations_data:
        organization = Organisation(
            int(org_data["client_id"]),
            roles[org_data["role"]],
            org_data["creation_date"],
            int(org_data["unp"]),
            org_data["name"],
        )
        organisations.append(organization)

with open("app.yaml", "r", encoding="utf8") as yamlfile:
    apps_data = yaml.load(yamlfile, Loader=yaml.FullLoader)["Apps"]
    for app_data in apps_data:
        app = App(int(app_data["client_id"]), app_data["name"], roles[app_data["role"]])
        apps.append(app)


def max_id():
    id_list = []
    id_user = max([int(i.client_id) for i in users])
    id_list.append(id_user)
    id_app = max([int(i.client_id) for i in apps])
    id_list.append(id_app)
    id_organisation = max([int(i.client_id) for i in organisations])
    id_list.append(id_organisation)
    max_id = max(id_list)
    return max_id


@app_flask.route("/")
def hello():
    return "Hello my friend. This is a ivanoff's authz service."


@app_flask.route("/api/v1/authz/health_check")
def check_health():
    return (
        jsonify({"status": "OK"}),
        200,
    )


@app_flask.route("/api/v1/users", methods=["GET"])
def read_users():
    if not request.headers.get("token"):
        return (
            jsonify({"status": "error", "message": "Token header not found"}),
            400,
        )
    elif request.headers.get("token"):
        # client_id = None
        token_data = json.loads(request.headers.get("token"))
        client_id = token_data["client_id"]
        for app in apps:
            if client_id == app.client_id:
                if "users" in (app.role.permissions):
                    if app.role.permissions["users"]["read"] == True:
                        return [user.to_dict() for user in users]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if client_id == user.client_id:
                if "users" in (user.role.permissions):
                    if user.role.permissions["users"]["read"] == True:
                        return [user.to_dict() for user in users]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if client_id == organisation.client_id:
                if "users" in (organisation.role.permissions):
                    if organisation.role.permissions["users"]["read"] == True:
                        return [user.to_dict() for user in users]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
    return (
        jsonify(
            {
                "status": "error",
                "message": f"No token user with id = {client_id}",
            }
        ),
        400,
    )


@app_flask.route("/api/v1/users/<int:client_id>", methods=["GET"])
def read_user(client_id):
    if not request.headers.get("token"):
        return jsonify({"status": "error", "message": "Token header not found"}), 400
    elif request.headers.get("token"):
        token_data = json.loads(request.headers.get("token"))
        cli_id = token_data["client_id"]
        for app in apps:
            if cli_id == app.client_id:
                if "users" in (app.role.permissions):
                    if app.role.permissions["users"]["read"] == True:
                        for user in users:
                            if client_id == user.client_id:
                                return user.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No user with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if cli_id == user.client_id:
                if "users" in (user.role.permissions):
                    if user.role.permissions["users"]["read"] == True:
                        for user in users:
                            if client_id == user.client_id:
                                return user.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No user with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if cli_id == organisation.client_id:
                if "users" in (organisation.role.permissions):
                    if organisation.role.permissions["users"]["read"] == True:
                        for user in users:
                            if client_id == user.client_id:
                                return user.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No user with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
    return (
        jsonify(
            {
                "status": "error",
                "message": f"No token user with id = {cli_id}",
            }
        ),
        400,
    )


@app_flask.route("/api/v1/organisations", methods=["GET"])
def read_organisations():
    if not request.headers.get("token"):
        return jsonify({"status": "error", "message": "Token header not found"}), 400
    elif request.headers.get("token"):
        token_data = json.loads(request.headers.get("token"))
        client_id = token_data["client_id"]
        for app in apps:
            if client_id == app.client_id:
                if "organisations" in (app.role.permissions):
                    if app.role.permissions["organisations"]["read"] == True:
                        return [
                            organisation.to_dict() for organisation in organisations
                        ]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if client_id == user.client_id:
                if "organisations" in (user.role.permissions):
                    if user.role.permissions["organisations"]["read"] == True:
                        return [
                            organisation.to_dict() for organisation in organisations
                        ]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if client_id == organisation.client_id:
                if "organisations" in (organisation.role.permissions):
                    if organisation.role.permissions["organisations"]["read"] == True:
                        return [
                            organisation.to_dict() for organisation in organisations
                        ]
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
    return (
        jsonify(
            {
                "status": "error",
                "message": f"No token user with id = {client_id}",
            }
        ),
        400,
    )


@app_flask.route("/api/v1/organisations/<int:client_id>", methods=["GET"])
def read_organisation(client_id):
    if not request.headers.get("token"):
        return jsonify({"status": "error", "message": "Token header not found"}), 400
    elif request.headers.get("token"):
        token_data = json.loads(request.headers.get("token"))
        cli_id = token_data["client_id"]
        for app in apps:
            if cli_id == app.client_id:
                if "organisations" in (app.role.permissions):
                    if app.role.permissions["organisations"]["read"] == True:
                        for organisation in organisations:
                            if client_id == organisation.client_id:
                                return organisation.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No organisation with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if cli_id == user.client_id:
                if "organisations" in (user.role.permissions):
                    if user.role.permissions["organisations"]["read"] == True:
                        for organisation in organisations:
                            if client_id == organisation.client_id:
                                return organisation.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No organisation with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if cli_id == organisation.client_id:
                if "organisations" in (organisation.role.permissions):
                    if organisation.role.permissions["organisations"]["read"] == True:
                        for organisation in organisations:
                            if client_id == organisation.client_id:
                                return organisation.to_dict()
                        else:
                            return (
                                jsonify(
                                    {
                                        "status": "error",
                                        "message": f"No organisation with id = {client_id}",
                                    }
                                ),
                                400,
                            )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
    return (
        jsonify(
            {
                "status": "error",
                "message": f"No token user with id = {cli_id}",
            }
        ),
        400,
    )


@app_flask.route("/api/v1/users", methods=["PUT"])
def add_user():
    if not request.headers.get("token"):
        return jsonify({"status": "error", "message": "Token header not found"}), 400
    elif request.headers.get("token"):
        token_data = json.loads(request.headers.get("token"))
        client_id = token_data["client_id"]
        for app in apps:
            if client_id == app.client_id:
                if "users" in (app.role.permissions):
                    if app.role.permissions["users"]["create"] == True:
                        new_user = {}
                        temp = {}
                        usersdata = {}
                        data = request.json
                        new_user["client_id"] = max_id() + 1
                        new_user["first_name"] = data["first_name"]
                        new_user["role"] = data["role"]
                        new_user["last_name"] = data["last_name"]
                        new_user["fathers_name"] = data["fathers_name"]
                        new_user["date_of_birth"] = data["date_of_birth"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Users"]
                        temp.append(new_user)
                        usersdata["Users"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(usersdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify({"status": "OK", "message": f"Add new user "}),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if client_id == user.client_id:
                if "users" in (user.role.permissions):
                    if user.role.permissions["users"]["create"] == True:
                        new_user = {}
                        temp = {}
                        usersdata = {}
                        data = request.json
                        new_user["client_id"] = max_id() + 1
                        new_user["first_name"] = data["first_name"]
                        new_user["role"] = data["role"]
                        new_user["last_name"] = data["last_name"]
                        new_user["fathers_name"] = data["fathers_name"]
                        new_user["date_of_birth"] = data["date_of_birth"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Users"]
                        temp.append(new_user)
                        usersdata["Users"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(usersdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify({"status": "OK", "message": f"Add new user "}),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if client_id == organisation.client_id:
                if "users" in (user.role.permissions):
                    if organisation.role.permissions["users"]["create"] == True:
                        new_user = {}
                        temp = {}
                        usersdata = {}
                        data = request.json
                        new_user["client_id"] = max_id() + 1
                        new_user["first_name"] = data["first_name"]
                        new_user["role"] = data["role"]
                        new_user["last_name"] = data["last_name"]
                        new_user["fathers_name"] = data["fathers_name"]
                        new_user["date_of_birth"] = data["date_of_birth"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Users"]
                        temp.append(new_user)
                        usersdata["Users"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(usersdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify({"status": "OK", "message": f"Add new user "}),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"No token user with id = {client_id}",
                    }
                ),
                400,
            )


@app_flask.route("/api/v1/organisations", methods=["PUT"])
def add_organisation():
    if not request.headers.get("token"):
        return jsonify({"status": "error", "message": "Token header not found"}), 400
    elif request.headers.get("token"):
        token_data = json.loads(request.headers.get("token"))
        client_id = token_data["client_id"]
        for app in apps:
            if client_id == app.client_id:
                if "organisations" in (app.role.permissions):
                    if app.role.permissions["organisations"]["create"] == True:
                        new_organisation = {}
                        temp = {}
                        organisationsdata = {}
                        data = request.json
                        new_organisation["client_id"] = max_id() + 1
                        new_organisation["role"] = data["role"]
                        new_organisation["creation_date"] = data["creation_date"]
                        new_organisation["unp"] = data["unp"]
                        new_organisation["name"] = data["name"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Organisations"]
                        temp.append(new_organisation)
                        organisationsdata["Organisations"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(organisationsdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify(
                                {"status": "OK", "message": f"Add new organisation"}
                            ),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for user in users:
            if client_id == user.client_id:
                if "organisations" in (user.role.permissions):
                    if user.role.permissions["organisations"]["create"] == True:
                        new_organisation = {}
                        temp = {}
                        organisationsdata = {}
                        data = request.json
                        new_organisation["client_id"] = max_id() + 1
                        new_organisation["role"] = data["role"]
                        new_organisation["creation_date"] = data["creation_date"]
                        new_organisation["unp"] = data["unp"]
                        new_organisation["name"] = data["name"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Organisations"]
                        temp.append(new_organisation)
                        organisationsdata["Organisations"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(organisationsdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify(
                                {"status": "OK", "message": f"Add new organisation"}
                            ),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        for organisation in organisations:
            if client_id == organisation.client_id:
                if "organisations" in (organisation.role.permissions):
                    if organisation.role.permissions["organisations"]["create"] == True:
                        new_organisation = {}
                        temp = {}
                        organisationsdata = {}
                        data = request.json
                        new_organisation["client_id"] = max_id() + 1
                        new_organisation["role"] = data["role"]
                        new_organisation["creation_date"] = data["creation_date"]
                        new_organisation["unp"] = data["unp"]
                        new_organisation["name"] = data["name"]
                        with open("users.json", "r", encoding="utf8") as userjson:
                            temp = json.loads(userjson.read())["Organisations"]
                        temp.append(new_organisation)
                        organisationsdata["Organisations"] = temp
                        with open("users.json", "r", encoding="utf8") as alljson:
                            all_data = json.loads(alljson.read())
                        all_data.update(organisationsdata)
                        with open("users.json", "w") as f:
                            json.dump(all_data, f, ensure_ascii=False, indent=2)
                        return (
                            jsonify(
                                {"status": "OK", "message": f"Add new organisation"}
                            ),
                            200,
                        )
                    else:
                        return (
                            jsonify({"status": "error", "message": "Access denied"}),
                            403,
                        )
                else:
                    return (
                        jsonify({"status": "error", "message": "Permission denied"}),
                        403,
                    )
        else:
            return (
                jsonify(
                    {
                        "status": "error",
                        "message": f"No token user with id = {client_id}",
                    }
                ),
                400,
            )


@app_flask.route(
    "/api/v1/<string:entity>/authz/<string:auth_permission>", methods=["GET"]
)
def check_permission(entity, auth_permission):
    try:
        if not request.headers.get("token"):
            return (
                jsonify({"status": "error", "message": "Token header not found"}),
                400,
            )
        elif request.headers.get("token"):
            token_data = json.loads(request.headers.get("token"))
            client_id = token_data["client_id"]
            for user in users:
                if client_id == user.client_id:
                    if entity in (user.role.permissions):
                        authorized = getattr(user.role[entity], auth_permission)
                        if authorized == True:
                            return (
                                jsonify({"status": "success", "message": "authorized"}),
                                200,
                            )
                        else:
                            return (
                                jsonify(
                                    {"status": "error", "message": "not authorized"}
                                ),
                                403,
                            )
                    else:
                        return (
                            jsonify(
                                {"status": "error", "message": "Permission denied"}
                            ),
                            403,
                        )
            for app in apps:
                if client_id == app.client_id:
                    if entity in (app.role.permissions):
                        authorized = getattr(app.role[entity], auth_permission)
                        if authorized == True:
                            return (
                                jsonify({"status": "success", "message": "authorized"}),
                                200,
                            )
                        else:
                            return (
                                jsonify(
                                    {"status": "error", "message": "not authorized"}
                                ),
                                403,
                            )
                    else:
                        return (
                            jsonify(
                                {"status": "error", "message": "Permission denied"}
                            ),
                            403,
                        )
            for organisation in organisations:
                if client_id == organisation.client_id:
                    if entity in (organisation.role.permissions):
                        authorized = getattr(organisation.role[entity], auth_permission)
                        if authorized == True:
                            return (
                                jsonify({"status": "success", "message": "authorized"}),
                                200,
                            )
                        else:
                            return (
                                jsonify(
                                    {"status": "error", "message": "not authorized"}
                                ),
                                403,
                            )
                    else:
                        return (
                            jsonify(
                                {"status": "error", "message": "Permission denied"}
                            ),
                            403,
                        )
            else:
                return (
                    jsonify(
                        {
                            "status": "error",
                            "message": f"No token user with id = {client_id}",
                        }
                    ),
                    400,
                )
    except Exception:
        return jsonify({"status": "error", "message": "not authorized"}), 403


if __name__ == "__main__":
    app_flask.run(host="0.0.0.0")
