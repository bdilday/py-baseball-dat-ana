import argparse
import requests
from functools import reduce
import pandas as pd
from pybbda.graphics.graphical_standings import plot_graphical_standings
from datetime import date, timedelta
from dateutil.parser import parse as datetime_parse
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

URL_FORMAT = (
    "https://statsapi.mlb.com/api/v1/standings"
    "?leagueId=103,104"
    "&season={season}"
    "&date={date_str}"
    "&standingsTypes=regularSeason,springTraining,firstHalf,secondHalf"
    "&hydrate=division,conference,sport,league,"
    "team(nextSchedule(team,gameType=[R,F,D,L,W,C],inclusive=false),"
    "previousSchedule(team,gameType=[R,F,D,L,W,C],inclusive=true))"
)

TODAY = date.today()
YESTERDAY = TODAY + timedelta(days=-1)


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--standings-date",
        "-d",
        required=False,
        type=lambda date_string: datetime_parse(date_string).date(),
        default=YESTERDAY,
    )
    return parser.parse_args()


def get_url(standings_date: date) -> str:
    return URL_FORMAT.format(season=standings_date.year, date_str=standings_date)


def process_team_record(team_record):
    return {
        "Team": team_record["team"]["teamName"],
        "W": team_record["wins"],
        "L": team_record["losses"],
        "RS_G": team_record["runsScored"] / team_record["gamesPlayed"],
        "RA_G": team_record["runsAllowed"] / team_record["gamesPlayed"],
    }


def process_record(record):
    lg_div = record["division"]["abbreviation"]
    return [
        {"lg_div": lg_div, **process_team_record(team_record)}
        for team_record in record["teamRecords"]
    ]


def main():
    args = _parse_args()
    url = get_url(args.standings_date)
    logger.info(f"fetching standings from {url}")
    payload = requests.get(url).json()
    logger.debug(payload)
    data = reduce(
        list.__add__, [process_record(record) for record in payload["records"]]
    )
    logger.debug(data)

    standings = pd.DataFrame(data)
    logger.info(standings)
    p = plot_graphical_standings(standings)
    print(p)


if __name__ == "__main__":
    main()
