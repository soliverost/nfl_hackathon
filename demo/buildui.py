
import pandas as pd
import numpy as np
from pyxley import UILayout
from pyxley.filters import SelectButton
from pyxley.filters import SliderInput
from helper import PlotlyLines
from helper import Images

def split_teams(datafile, players, dist):
    df = pd.read_csv(datafile)
    df = pd.merge(df, players, on=["team", "game", "nflId"],
        how="inner", sort=False)

    usecols = ["team", "game", "nflId", "ngsId"]
    ignore = [c for c in players.columns if c not in usecols]
    use = [c for c in dist.columns if c not in ignore]

    df = pd.merge(df, dist.ix[:, use], on=["team", "game", "nflId", "ngsId"],
        how="left", sort=False)

    home = df.loc[df.team == "home"].drop("team", 1)
    home["pRank"] = home.groupby(["game", "ngsId"])["nflId"].rank()


    away = df.loc[df.team == "away"].drop("team", 1)
    away["pRank"] = away.groupby(["game", "ngsId"])["nflId"].rank()
    away = away.rename(columns={
        "x": "x_away", "y": "y_away",
        "position": "position_away",
        "nflId": "away_nflId",
        "dist": "dist_away"
    })

    _joincols = ["game", "ngsId", "pRank"]

    df = pd.merge(home, away, on=_joincols, how="inner", sort=False)

    _ids = df.groupby(["game", "ngsId"]).size().reset_index()
    _ids["new_index"] = _ids.groupby("game")['ngsId'].rank(
        ).astype("int").astype("str")

    df = pd.merge(df, _ids, on=["game", "ngsId"], how='inner', sort=False)
    df.new_index = df.new_index.astype("int").astype("str")

    df["dist"] = (200.* (df["dist"] - df["dist"].min() ) /
        (df["dist"].max() - df["dist"].min()))
    df["dist_away"] = (200.* (df["dist_away"] - df["dist_away"].min() ) /
        (df["dist_away"].max() - df["dist_away"].min()))
    df["dist"] = df["dist"].fillna(24)
    df["dist_away"] = df["dist_away"].fillna(24)
    df["dist"].loc[df["dist"] < 24] = 24
    df["dist_away"].loc[df["dist_away"] < 24] = 24
    return df, _ids

def fatigue(datafile):
    df = pd.read_csv(datafile)
    return df

def distance_measures(datafile, fatigue, players):
    df = pd.read_csv(datafile)
    xf = pd.merge(df, fatigue, how="inner",
        sort=False, on=["game","team","ngsId"])
    xf["dist"] = np.sqrt((xf["distmean"] - xf["total_dist"])**2.)

    df = pd.merge(xf, players, how="inner", sort=False,
        on=["game", "team", "nflId"])

    return df

def load_players(datafile):
    return pd.read_csv(datafile)

def make_ui(datafiles):
    # Make a UI
    ui = UILayout(
        "FilterChart",
        "pyxley",
        "component_id",
        filter_style="''")

    ff = fatigue(datafiles["scores"])
    pf = load_players(datafiles["players"])
    sf = distance_measures(datafiles["distance"], ff, pf)

    df, _ids = split_teams(datafiles["locations"], pf, sf)

    sf = pd.merge(sf, _ids, on=["game", "ngsId"], how='inner', sort=False)
    _onfield = sf.loc[sf.isOnField == True].reset_index(drop=True)
    _offfield = sf.loc[sf.isOnField == False].reset_index(drop=True)

    sldr = SliderInput("new_index", 1, int(df["new_index"].max()), "new_index", "0")

    # Read in the data and stack it, so that we can filter on columns

    # Make a Button
    games = ["game1", "game2", "game3"]
    btnG = SelectButton("Game", games, "game", "game1")
    # Make a FilterFrame and add the button to the UI
    ui.add_filter(sldr)
    ui.add_filter(btnG)

    init_params = {
        "game": "game1",
        "new_index": "1"
    }

    dm = PlotlyLines([["y", "x"], ["y_away", "x_away"]], df,
        labels=["position", "position_away"],
        names=["Home", "Away"],
        init_params=init_params,
        layout={
            "hovermode": "closest",
            "plot_bgcolor": 'rgba(44,94,79,0.7)',
            "xaxis": {"range": [0, 53]},
            "paper_bgcolor": 'rgba(44, 94, 79, 0.0)',
        })
    ui.add_chart(dm)

    imgs = Images(init_params, _onfield, _offfield)
    ui.add_chart(imgs)
    return ui
