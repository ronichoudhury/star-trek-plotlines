import json
import tangelo

from startrek import DBSession
from startrek import Episode


def count_barchart(sort):
    session = DBSession()

    count = {}
    episodes = session.query(Episode)
    for ep in episodes:
        seen = set()
        for writer in ep.teleplay:
            count[writer] = count.get(writer, 0) + 1
            seen.add(writer)

        for writer in ep.story:
            if writer not in seen:
                count[writer] = count.get(writer, 0) + 1

    results = [{"name": r.name, "count": count[r]} for r in sorted(count.keys(), key=lambda x: x.id)]
    if sort:
        results.sort(key=lambda x: x["count"], reverse=True)

    return results


@tangelo.types(sort=json.loads)
def run(plot_type, sort=False):
    if plot_type == "count":
        return count_barchart(sort=sort)
    else:
        tangelo.http_status(400, "Illegal plot type")
        return {"error": "Illegal plot type: %s" % (plot_type)}
