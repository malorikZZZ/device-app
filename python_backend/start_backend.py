import asyncio
from sanic import Sanic, response
from sanic.response import json
from sanic.exceptions import abort
from sanic_cors import CORS
from aiopeewee import AioModel, AioMySQLDatabase, model_to_dict
from peewee import CharField, TextField, BooleanField, ForeignKeyField, PrimaryKeyField, SmallIntegerField
from datetime import datetime
from libs.check_auth import Auth_checker

db = AioMySQLDatabase('device', user='test', password='test', host='127.0.0.1', port=3306)

valid_status = ['new', 'in_progress', 'finished', 'declined', 'expired']
master_roles = ['bormann', 'device_manager']
invalid_status_for_reserv = ['new', 'in_progress']


class Devices_Category(AioModel):
    id = PrimaryKeyField()
    name = CharField(max_length=301, index=True, unique=True)

    class Meta:
        database = db


class Devices(AioModel):
    id = PrimaryKeyField()
    name = CharField(max_length=301, index=True, unique=True)
    description = TextField()
    login = CharField(max_length=100)
    created = CharField(max_length=25, null=True)
    active = BooleanField(null=False)
    available = BooleanField(null=False)
    image_url = TextField()
    category = ForeignKeyField(Devices_Category, to_field='id')

    class Meta:
        database = db


class Reserv(AioModel):
    id = PrimaryKeyField()
    status = CharField(max_length=301, index=True, unique=True)
    author = SmallIntegerField()
    employee = SmallIntegerField()
    device = ForeignKeyField(Devices, to_field='id')
    day = CharField(max_length=20)
    created = CharField(max_length=25, null=True)

    class Meta:
        database = db


app = Sanic(__name__)
loop = asyncio.get_event_loop()
app.config['CORS_AUTOMATIC_OPTIONS'] = True
CORS(app)


def check_int(headers, params_name):
    for param in params_name.replace(' ', '').split(','):
        try:
            int(headers[param])
        except ValueError:
            return json(
                {"Error": "parameter " + param + " must be integer, current " + param + "='" + headers[param] + "'",
                 "status": 422}, status=422)


def bool_to_int_or_break(header_value, header_name):
    try:
        flag = bool(header_value)
    except ValueError:
        return json({
                        "Error": "parameter " + header_name + " must be boolean, current " + header_name + "='" + header_value + "'",
                        "status": 422}, status=422)
    if flag:
        return 1
    else:
        return 0


def compare_statuses(incoming_statuses):
    if len(incoming_statuses) > 0:
        good = set(incoming_statuses) & set(valid_status)
        bad = set(incoming_statuses) - set(valid_status)
        if len(good) > 0:
            return good, bad
        else:
            return json({
                            "Error": "statuses must be in '" + valid_status + "', current bad statuses=" + bad + " ...or something wrong with service",
                            "status": 418}, status=418)
    else:
        return json({"Error": "statuses must be in '" + valid_status + "', current list of statuses is empty",
                     "status": 422}, status=422)


@app.middleware('request')
async def jump_auth(request):
    if 'authorization' in request.headers.keys():
        token = request.headers['authorization']
        result = Auth_checker(token)
        if not result:
            return response.json({"Error": "Unauthorized", "status": 401}, status=401)
        else:
            pass
    else:
        return response.json({"Error": "Unauthorized. Reason: missing token", "status": 401}, status=401)


@app.listener('before_server_start')
async def setup(app, loop):
    # create connection pool
    await db.connect(loop)
    # create table if not exists
    await db.create_tables([Devices, Devices_Category, Reserv], safe=True)


@app.listener('before_server_stop')
async def stop(app, loop):
    # close connection pool
    await db.close()


@app.route("/add_devices_category", methods=["GET"])
async def set_devices_category(request):
    await Devices_Category.create(id=1, name='smartphone')
    await Devices_Category.create(id=2, name='smarttv')
    await Devices_Category.create(id=3, name='smartwatch')
    await Devices_Category.create(id=4, name='smartpad')
    await Devices_Category.create(id=5, name='smartnotebook')
    return json("ok")


@app.route("/add_devices", methods=["POST"])
async def set_devices(request):
    d = await Devices.create(**request.json)
    return json(await model_to_dict(d))


@app.route("/add_reservs", methods=["POST"])
async def set_reservs(request):
    d = await Reserv.create(**request.json)
    return json(await model_to_dict(d))


@app.route("/reservation", methods={'GET', 'POST'})
async def reservation(request):
    if request.method == 'GET':
        if 'page' in request.headers.keys() and 'size' in request.headers.keys() and 'statuses' in request.headers.keys():
            check_int(request.headers, 'page, size')
            good_stat, bad_stat = compare_statuses(request.headers['statuses'])

            total = await Reserv.select().where(Reserv.status in good_stat).order_by(
                Reserv.created.desc()).paginate(int(request.headers['page']), int(request.headers['size'])).limit(
                10000).count()

            reservs = Reserv.select().where(Reserv.status in good_stat).order_by(
                Reserv.created.desc()).paginate(int(request.headers['page']), int(request.headers['size'])).limit(10000)

            page = request.headers['page']
            size = request.headers['size']

        elif 'page' in request.headers.keys() and 'size' in request.headers.keys() and 'statuses' not in request.headers.keys():
            check_int(request.headers, 'page, size')
            total = await Reserv.select().order_by(Reserv.created.desc()).paginate(
                int(request.headers['page']), int(request.headers['size'])).limit(10000)

            reservs = Reserv.select().order_by(Reserv.created.desc()).paginate(
                int(request.headers['page']),
                int(request.headers[
                        'size'])).limit(10000)

            page = request.headers['page']
            size = request.headers['size']

        elif (
                        'page' not in request.headers.keys() or 'size' not in request.headers.keys()) and 'active' in request.headers.keys():
            good_stat, bad_stat = compare_statuses(request.headers['statuses'])

            total = await Reserv.select().where(Reserv.status in good_stat).order_by(
                Reserv.created.desc()).limit(10000).count()

            reservs = Reserv.select().where(Reserv.status in good_stat).order_by(
                Reserv.created.desc()).limit(
                10000)
            page = 1
            size = total

        else:
            total = await Reserv.select().order_by(Reserv.created.desc()).limit(10000).count()

            reservs = Reserv.select().order_by(Reserv.created.desc()).limit(10000)
            page = 1
            size = total

        right_reservs = [await model_to_dict(res) async for res in reservs]
        for i in range(len(right_reservs)):
            right_reservs[i]['device'] = right_reservs[i]['device']['id']
        return json({'total': total,
                     'page': page,
                     'size': size,
                     'items': right_reservs})
    elif request.method == 'POST':
        body_param = request.json
        if len(body_param) < 3 or "employee" not in body_param or "device" not in body_param or "day" not in body_param:
            return json({"Error": "Check params into body, current param=" + body_param, "status": 422}, status=422)
        else:
            check_int(body_param, "employee, device")
            if len(body_param["day"]) > 0:
                id_current_user = get_check_current_user(request.headers['authorization'], body_param['employee'])
                check_reserv = await check_reserv_status(body_param['device'], body_param["day"])
                if not check_reserv:
                    res = await Reserv.create(created=str(datetime.now().strftime('%Y-%m-%dT%H:%M:%S %Z')),
                                            status="new",
                                            author=int(str(id_current_user)),
                                            employee=int(body_param['employee']),
                                            device=int(body_param['device']),
                                            day=str(body_param["day"]))
                    return json(await model_to_dict(res))

                else:
                    return json(
                        {"Error": "Check params into body, current param=" + str(body_param) + ". Bad param is 'day'",
                        "status": 422},
                        status=422)

    else:
        return response.json({"Error": "Not found.", "status": 404}, status=404)


def get_check_current_user(token, user):
    data = Auth_checker(token).data
    current = data['employee_id']
    if current != user:
        if set(master_roles) & set(data['role']):
            if 'int' in str(type(data['employee_id'])):
                return int(data['employee_id'])
        else:
            abort(401)
    else:
        if 'int' in str(type(data['employee_id'])):
            return int(data['employee_id'])


async def check_reserv_status(id, day):
    device = await Devices.select().where(Devices.id == id)
    if device:
        reserv_count = await Reserv.select().where((Reserv.device == id) & (Reserv.day == day)).count()
        if reserv_count == 0:
            return
        else:
            reserv = await model_to_dict(await Reserv.select().where((Reserv.device == id) & (Reserv.day == day)).first())
        if reserv and reserv['status'] not in invalid_status_for_reserv:
            pass
        else:
            return response.json({"Error": "Can't add reservation, current reservation status='" + reserv['status'] +
                        " in list of invalid status for reserv " + str(invalid_status_for_reserv), "status": 422}, status=422)
    else:
        return response.json({"Error": "Not found id, current id=" + id, "status": 404}, status=404)


@app.route("/reservation/<id>/decline", methods=["POST"])
async def decline_reserv(request, id):
    try:
        int(id)
    except ValueError:
        return json({"Error": "parameter id must be integer, current id=" + id,
                     "status": 422}, status=422)

    data = Auth_checker(request.headers['authorization']).data
    reserv = await model_to_dict(await Reserv.select().where(Reserv.id == id).first())
    if (data['employee_id'] == reserv['author'] and reserv['status'] == 'new') or set(master_roles) & set(data['role']):
        if reserv:
            try:
                await Reserv.delete().where(Reserv.id == int(id))
            except:
                return json({"Error": "something wrong...",
                             "status": 418}, status=418)
            return json(reserv)
        else:
            return response.json({"Error": "Not found. Reason: don't see into base current id=" + id, "status": 404},
                                 status=404)
    else:
        return json({"Error": "Forbidden.", "status": 403}, status=403)


@app.route("/device", methods=["GET"])
async def get_device_list(request):
    if 'page' in request.headers.keys() and 'size' in request.headers.keys() and 'active' in request.headers.keys():
        check_int(request.headers, 'page, size')
        active = bool_to_int_or_break(request.headers['active'], 'active')
        total = await Devices.select().where(Devices.active == active).order_by(
            Devices.created.desc()).paginate(int(request.headers['page']), int(request.headers['size'])).count()

        devices = Devices.select().where(Devices.active == active).order_by(
            Devices.created.desc()).paginate(int(request.headers['page']), int(request.headers['size']))
        page = request.headers['page']
        size = request.headers['size']

    elif 'page' in request.headers.keys() and 'size' in request.headers.keys() and 'active' not in request.headers.keys():
        check_int(request.headers, 'page, size')
        total = await Devices.select().order_by(Devices.created.desc()).paginate(
            int(request.headers['page']), int(request.headers['size'])).count()

        devices = Devices.select().order_by(Devices.created.desc()).paginate(
            int(request.headers['page']), int(request.headers['size']))
        page = request.headers['page']
        size = request.headers['size']

    elif (
            'page' not in request.headers.keys() or 'size' not in request.headers.keys()) and 'active' in request.headers.keys():
        active = bool_to_int_or_break(request.headers['active'], 'active')
        total = await Devices.select().where(Devices.active == active).order_by(
            Devices.created.desc()).limit(10000).count()

        devices = Devices.select().where(Devices.active == active).order_by(
            Devices.created.desc()).limit(10000)
        page = 1
        size = total

    else:
        total = await Devices_Category.select().order_by(Devices.created.desc()).limit(10000).count()

        devices = Devices.select().order_by(Devices.created.desc()).limit(10000)
        page = 1
        size = total

    right_devices = [await model_to_dict(res) async for res in devices]
    for i in range(len(right_devices)):
        right_devices[i]['category'] = right_devices[i]['category']['id']

    return json({'total': total,
                 'page': page,
                 'size': size,
                 'items': right_devices})


@app.route("/device/<id>/report", methods=["POST"])
async def get_device_report(request, id):
    check_int({'id': id}, 'id')
    data = request.json
    if 'availability' in data.keys() and len(data['availability']):
        try:
            stat = await Devices.update(Devices.id).where(Devices.id == int(id))
            if stat:
                return json(stat)
        except:
            return response.json(
                {"Error": "Not found. Reason: don't see current id (" + id + ") into base", "status": 404}, status=404)

    availability = await Devices.select(Devices.available).where(Devices.id == int(id))
    return json({await model_to_dict(availability)})


@app.route("/device_category", methods=["GET"])
async def get_device_category_list(request):
    if 'page' in request.headers.keys() and 'size' in request.headers.keys():
        check_int(request.headers, 'page, size')
        total = await Devices_Category.select().order_by(Devices_Category.id.desc()).paginate(
            int(request.headers['page']), int(request.headers['size'])).count()
        dc = Devices_Category.select().order_by(Devices_Category.id.desc()).paginate(int(request.headers['page']),
                                                                                     int(request.headers['size']))
        page = request.headers['page']
        size = request.headers['size']

    else:
        total = await Devices_Category.select().order_by(Devices_Category.id.desc()).limit(10000).count()
        dc = Devices_Category.select().order_by(Devices_Category.id.desc()).limit(10000)
        page = 1
        size = total

    return json({'total': total,
                 'page': page,
                 'size': size,
                 'items': [await model_to_dict(dev_cat) async for dev_cat in dc]})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3333, workers=1, debug=False)
