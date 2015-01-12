import csv
import datetime
import sys

from sqlalchemy import create_engine
engine = create_engine("sqlite:///stplots.db", echo=True, convert_unicode=True)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker(bind=engine)

# Column types.
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import Integer
from sqlalchemy import String

# Other database necessities.
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

episode_teleplays = Table("episode_teleplays", Base.metadata,
                          Column("episode_id", Integer, ForeignKey("episodes.id")),
                          Column("teleplay_id", Integer, ForeignKey("people.id")))

episode_stories = Table("episode_stories", Base.metadata,
                        Column("episode_id", Integer, ForeignKey("episodes.id")),
                        Column("story_id", Integer, ForeignKey("people.id")))

episode_directors = Table("episode_directors", Base.metadata,
                          Column("episode_id", Integer, ForeignKey("episodes.id")),
                          Column("director_id", Integer, ForeignKey("people.id")))

episode_plots = Table("episode_plots", Base.metadata,
                      Column("episode_id", Integer, ForeignKey("episodes.id")),
                      Column("plot_id", Integer, ForeignKey("plots.id")))


class Episode(Base):
    __tablename__ = "episodes"

    id = Column(Integer, primary_key=True)
    season = Column(Integer)
    episode = Column(Integer)
    title = Column(String)
    airdate = Column(Date)
    teleplay = relationship("Person", secondary=episode_teleplays, backref="teleplays")
    story = relationship("Person", secondary=episode_stories, backref="stories")
    director = relationship("Person", secondary=episode_directors, backref="directors")
    stardate = Column(String)
    plot = relationship("Plot", secondary=episode_plots, backref="plots")
    url = Column(String)

    def __repr__(self):
        return (u"Episode('%s')" % (self.title)).encode("utf-8")


class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return (u"Person('%s')" % (self.name)).encode("utf-8")


class Plot(Base):
    __tablename__ = "plots"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return (u"Plot('%s')" % (self.name)).encode("utf-8")


def main():
    if len(sys.argv) < 4:
        print >>sys.stderr, "usage: build-db.py <episode-file> <people-file> <plot-file>"
        return 1

    episode_file, people_file, plot_file = sys.argv[1:4]

    try:
        with open(episode_file) as episodes_f:
            with open(people_file) as people_f:
                with open(plot_file) as plots_f:
                    episodes = list(csv.reader(episodes_f))
                    people = list(csv.reader(people_f))
                    plots = list(csv.reader(plots_f))
    except IOError as e:
        print >>sys.stderr, "error: %s" % (e)
        return 1

    Base.metadata.create_all(engine)

    session = DBSession()

    people_rec = {}
    for i, name in people[1:]:
        i = int(i)

        p = Person(id=i, name=name.decode("utf-8"))

        people_rec[i] = p
        session.add(p)

    plots_rec = {}
    for i, plot in plots[1:]:
        i = int(i)

        p = Plot(id=i, name=plot)

        plots_rec[i] = p
        session.add(p)

    for i, season, ep, title, airdate, teleplay, story, director, stardate, plot, url in episodes[1:]:
        i = int(i)
        season = int(season)
        ep = int(ep)

        month, day, year = airdate.split("/")
        month = "%02d" % (int(month))
        day = "%02d" % (int(day))
        airdate = datetime.datetime.strptime("%s/%s/%s" % (month, day, year), "%m/%d/%Y")

        teleplay = map(lambda writer: people_rec[int(writer)], teleplay.split(","))
        story = map(lambda writer: people_rec[int(writer)], story.split(","))
        director = map(lambda writer: people_rec[int(writer)], director.split(","))
        plot = map(lambda plot: plots_rec[int(plot)], filter(None, plot.split(",")))

        ep = Episode(id=int(i), season=season, episode=ep, airdate=airdate, teleplay=teleplay, story=story, director=director, plot=plot, url=url)
        session.add(ep)

    session.commit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
