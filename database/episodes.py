import datetime
import json
import tangelo

from startrek import DBSession
from startrek import Episode


def scatterplot(*fields, **kw):
    def get_type_converter(field):
        if field == "airdate":
            return lambda airdate: (airdate - datetime.date.fromtimestamp(0)).total_seconds() * 1000.0
        elif field == "stardate":
            def average_stardate(datestring):
                if datestring == "":
                    return None

                dates = datestring.split(",")
                return sum(map(float, dates)) / len(dates)
            return average_stardate
        else:
            return lambda x: x

    session = DBSession()

    seasons = kw.get("seasons")
    if seasons is None:
        eps = session.query(Episode)
    else:
        try:
            seasons = json.loads(seasons)
            if not isinstance(seasons, list):
                raise ValueError("not a list")
        except ValueError as e:
            tangelo.http_status(400, "Bad argument")
            return {"error": e}

        eps = session.query(Episode).filter(Episode.season.in_(seasons))

    if eps.count() > 0:
        ep = eps[0]

        for f in fields:
            if f not in ep.__dict__:
                tangelo.http_status(400, "Bad field name")
                return {"error": "Bad field name: %s" % (f)}

        eps = [{f: get_type_converter(f)(r.__dict__[f]) for f in fields} for r in eps]

    return filter(lambda r: all(r[f] is not None for f in fields), eps)


def run(plot_type, **query):
    if plot_type == "scatter":
        if "seasons" in query:
            return scatterplot(query.get("x"), query.get("y"), "title", seasons=query.get("seasons"))
        else:
            return scatterplot(query.get("x"), query.get("y"), "title")
    else:
        tangelo.http_status(400, "Illegal plot type")
        return {"error": "Illegal plot type: %s" % (plot_type)}
