import datetime
import tangelo

from startrek import DBSession
from startrek import Episode


def scatterplot(x_field, y_field, x_type=None, y_type=None):
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
    eps = session.query(Episode)

    if eps.count() > 0:
        ep = eps[0]

        if x_field not in ep.__dict__:
            tangelo.http_status(400, "Bad field name")
            return {"error": "Bad field name: %s" % (x_field)}

        if y_field not in ep.__dict__:
            tangelo.http_status(400, "Bad field name")
            return {"error": "Bad field name: %s" % (y_field)}

        x_type = get_type_converter(x_field)
        y_type = get_type_converter(y_field)

        eps = [{"x": x_type(r.__dict__[x_field]), "y": y_type(r.__dict__[y_field])} for r in eps]

    return eps


def run(plot_type, **query):
    if plot_type == "scatter":
        return scatterplot(query.get("x"), query.get("y"))
    else:
        tangelo.http_status(400, "Illegal plot type")
        return {"error": "Illegal plot type: %s" % (plot_type)}
