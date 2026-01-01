import streamlit as st
import pandas as pd
import numpy as np
import math


# sidebar navigation
st.sidebar.title("""Page Navigator""")
page = st.sidebar.radio("Go to", ("Standings", "Roster View"))


player_info_df = pd.read_csv("player_info.csv", encoding="utf-8", sep = ",", header=0)
rosters_list_df = pd.read_csv("rosters_list.csv", encoding="utf-8", sep = ",", header=0).iloc[:,0:8]
team_odds_df = pd.read_csv("team_odds.csv", encoding="utf-8", sep = ",", header=0)


team_odds_short = team_odds_df[["TEAM", "REMAINING"]]
rosters_pts_df = rosters_list_df.merge(player_info_df, on = ["POS", "PLAYER"], how="left")\
    .merge(team_odds_short, on = "TEAM", how = "left")
rosters_pts_df["FUT_PTS"] =  rosters_pts_df["PPG"] * rosters_pts_df["REMAINING"]
rosters_pts_df["PROJ_PTS"] = np.round(rosters_pts_df["TOTAL_PTS"] + rosters_pts_df["FUT_PTS"], 2)
rosters_pts_df["STILL_ALIVE"] = np.where(rosters_pts_df["REMAINING"]>0,1,0)

standings_df = rosters_pts_df.groupby("MANAGER", as_index=False)\
    .agg({
        "TOTAL_PTS":"sum",
        "PROJ_PTS":"sum"
    })\
    .rename(columns = {
        "MANAGER": "Fantasy Team",
        "TOTAL_PTS": "Actual Points",
        "PROJ_PTS": "Projected Points"
    })

roster_view_df = rosters_pts_df[["MANAGER", "PLAYER", "POS", "TEAM", "TOTAL_PTS", "PROJ_PTS", "STILL_ALIVE", "PPG", "REMAINING", "WC_PTS", "DIV_PTS", "CONF_PTS", "SB_PTS"]]
roster_view_df["REMAINING"] = np.round(roster_view_df["REMAINING"], 2)
roster_view_df = roster_view_df.rename(columns={
        "MANAGER": "Fantasy Team",
        "PLAYER": "Player",
        "TEAM": "TM",
        "TOTAL_PTS": "Actual Points",
        "PROJ_PTS": "Projected Points",
        "STILL_ALIVE": "Still Alive",
        "PPG": "Reg Szn PPG",
        "REMAINING": "Exp Games Remaining",
        "WC_PTS": "WC PTS",
        "DIV_PTS": "DIV PTS",
        "CONF_PTS": "CONF PTS",
        "SB_PTS": "SB PTS"
    })

unique_fantasy_teams = sorted(pd.unique(roster_view_df["Fantasy Team"]))
                              



def standings_page():

    st.title("Standings")

    st.write("Here are our current standings!")

    st.write("Projected points are based on a team's current expected games played and the player's half ppr ppg from Weeks 11-17")

    st.divider()

    sort_choice = st.selectbox("Sort by:",
                               options = ["Projected Points", "Actual Points"],
                               index = 0)

    displayed_df = standings_df.sort_values(sort_choice, ascending=False)

    st.dataframe(displayed_df)

    st.divider()


def roster_view_page():
    

    st.title("Roster View")

    st.write("Take a look at things for each fantasy team and their players")

    st.divider()

    team_filter = st.selectbox("Fantasy Team",
                               options = unique_fantasy_teams,
                               index = 0)
    
    view_choice = st.selectbox("View",
                               options = ["Shortened", "Expanded"],
                               index = 0)
    
    shortened_roster_df = roster_view_df.loc[roster_view_df["Fantasy Team"]==team_filter]
    shortened_roster_df = shortened_roster_df.drop(["Fantasy Team", "Reg Szn PPG", "Exp Games Remaining", "WC PTS", "DIV PTS", "CONF PTS", "SB PTS"], axis=1)

    expanded_roster_df = roster_view_df.loc[roster_view_df["Fantasy Team"]==team_filter]
    expanded_roster_df = expanded_roster_df.drop("Fantasy Team", axis=1)

    if view_choice == "Shortened":
        st.dataframe(shortened_roster_df)
    else:
        st.dataframe(expanded_roster_df)

    st.divider()



# display the selected page
if page == "Standings":
    standings_page()
elif page == "Roster View":
    roster_view_page()


