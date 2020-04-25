from pybaseballdatana.data import nullable_int, LahmanData


def get_age(stats_df, people_df=None):
    if people_df is None:
        print("oh no, people_df is none")
        people_df = LahmanData().people
    return (
        stats_df.merge(
            people_df.filter(["playerID", "birthYear"], axis=1), on="playerID"
        )
        .assign(age=lambda row: (row.yearID - row.birthYear).astype(nullable_int))
        .filter(["playerID", "yearID", "age"], axis=1)
    )
