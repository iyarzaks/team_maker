import streamlit as st
import json
import random
from typing import List, Dict, Tuple
import pandas as pd
import os

class Player:
    def __init__(self, name: str, rating: float, present: bool = False):
        self.name = name
        self.rating = rating
        self.present = present

    def to_dict(self):
        return {
            'name': self.name,
            'rating': self.rating,
            'present': self.present
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['rating'], data.get('present', False))

def load_initial_players():
    """טעינת שחקנים מהתמונות שהועלו"""
    initial_players = [
        # מהתמונה הראשונה
        ("גלעד", 2.0), ("דניאל בינוק", 3.0), ("זהורי", 2.0), ("זוהר", 4.0),
        ("זרבלי", 3.5), ("טל בינוק", 4.5), ("יונתן", 1.5), ("יוסי", 4.5),
        ("יכין מן", 3.0), ("יקיר", 3.5), ("ירום", 1.0), ("לוטנו", 1.5),
        ("ליאור בינוק", 4.0), ("מושי", 3.0), ("מבדהם", 2.0),

        # מהתמונה השנייה
        ("אביב", 1.5), ("אביחי", 3.0), ("אדם קרני", 1.0), ("אהוד", 3.0),
        ("אורי", 1.5), ("איציק דקל", 3.5), ("איתמר אוחיון", 2.5), ("אלדד זהן", 1.0),
        ("אלון ספקטור", 3.0), ("אלירן", 3.0), ("אסי גוטהרד", 3.5), ("בר רחמני", 5.0),
        ("גד", 3.0), ("דעוון חרן", 2.0), ("גלעד", 2.0),

        # מהתמונה השלישית
        ("מתן אברהם", 3.5), ("מתן קדוש", 2.5), ("נדב נוביצק", 2.0), ("ניתאי", 4.5),
        ("סער זיו", 1.5), ("עדן כהן", 3.5), ("עומר אלטונו", 3.0), ("עומרי יעקב", 4.5),
        ("עילאי", 5.0), ("צורי", 4.0), ("קוסטה", 3.0), ("רביד", 4.5),
        ("רוח טל", 3.0), ("רעי נוביצק", 3.5), ("שלי", 4.0),

        # מהתמונה הרביעית
        ("שרון גולדבר", 3.0), ("תם קטלן", 4.0)
    ]

    # הסרת כפילויות על בסיס שם
    unique_players = {}
    for name, rating in initial_players:
        if name not in unique_players:
            unique_players[name] = rating

    players = [Player(name, rating) for name, rating in unique_players.items()]
    players.sort(key=lambda p: p.name)
    return players

def save_data(players):
    """שמירת נתונים לקובץ"""
    data = {
        'players': [player.to_dict() for player in players]
    }
    with open('players_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data():
    """טעינת נתונים מקובץ"""
    try:
        if os.path.exists('players_data.json'):
            with open('players_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            return [Player.from_dict(player_data) for player_data in data['players']]
    except Exception:
        pass
    return load_initial_players()

def balance_teams(players: List[Player], num_teams: int) -> List[List[Player]]:
    """אלגוריתם ליצירת קבוצות מאוזנות"""
    # מיון שחקנים לפי דירוג (מהגבוה לנמוך)
    sorted_players = sorted(players, key=lambda p: p.rating, reverse=True)

    # יצירת קבוצות ריקות
    teams = [[] for _ in range(num_teams)]
    team_ratings = [0.0] * num_teams

    # חלוקת השחקנים
    for player in sorted_players:
        # מציאת הקבוצה עם הדירוג הנמוך ביותר
        min_rating_team = min(range(num_teams), key=lambda i: team_ratings[i])

        # הוספת השחקן לקבוצה
        teams[min_rating_team].append(player)
        team_ratings[min_rating_team] += player.rating

    return teams

def main():
    # הגדרת הדף
    st.set_page_config(
        page_title="מנהל קבוצות כדורגל",
        page_icon="⚽",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS מותאם אישית
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #27ae60, #2ecc71);
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stats-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #3498db;
        color: #2c3e50;
    }

    .team-container {
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        color: white;
        font-weight: bold;
    }

    .team-yellow {
        background: linear-gradient(135deg, #f1c40f, #f39c12);
        border-color: #e67e22;
        color: #2c3e50;
    }

    .team-red {
        background: linear-gradient(135deg, #e74c3c, #c0392b);
        border-color: #922b21;
        color: white;
    }

    .team-blue {
        background: linear-gradient(135deg, #3498db, #2980b9);
        border-color: #1f4e79;
        color: white;
    }

    .team-black {
        background: linear-gradient(135deg, #34495e, #2c3e50);
        border-color: #1a252f;
        color: white;
    }

    .team-container h4 {
        font-weight: bold;
        margin-bottom: 10px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .team-container p {
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .team-container ul {
        font-weight: bold;
    }

    .team-container li {
        font-weight: bold;
        margin-bottom: 5px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }

    .team-yellow h4, .team-yellow p, .team-yellow li {
        color: #2c3e50;
    }

    .player-present {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
    }

    .player-absent {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

    # כותרת ראשית
    st.markdown("""
    <div class="main-header">
        <h1>⚽ מנהל קבוצות כדורגל ⚽</h1>
        <p>ניהול שחקנים וחלוקת קבוצות מאוזנות</p>
    </div>
    """, unsafe_allow_html=True)

    # אתחול session state
    if 'players' not in st.session_state:
        st.session_state.players = load_data()

    # Sidebar - ניהול שחקנים
    with st.sidebar:
        st.header("🎮 ניהול שחקנים")

        # הוספת שחקן חדש
        st.subheader("➕ הוסף שחקן חדש")
        with st.form("add_player"):
            new_name = st.text_input("שם השחקן")
            new_rating = st.slider("דירוג השחקן", 1.0, 5.0, 3.0, 0.5)
            if st.form_submit_button("הוסף שחקן"):
                if new_name and not any(p.name == new_name for p in st.session_state.players):
                    st.session_state.players.append(Player(new_name, new_rating))
                    st.session_state.players.sort(key=lambda p: p.name)
                    st.success(f"השחקן {new_name} נוסף בהצלחה!")
                    st.rerun()
                elif new_name:
                    st.error("שחקן עם שם זה כבר קיים!")
                else:
                    st.error("אנא הזן שם שחקן!")

        st.divider()

        # ניהול נוכחות מהיר
        st.subheader("⚡ פעולות מהירות")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ סמן הכל", use_container_width=True):
                for player in st.session_state.players:
                    player.present = True
                st.rerun()

        with col2:
            if st.button("❌ בטל הכל", use_container_width=True):
                for player in st.session_state.players:
                    player.present = False
                st.rerun()

        st.divider()

        # שמירה וטעינה
        st.subheader("💾 נתונים")
        if st.button("🔄 איפוס לברירת מחדל", use_container_width=True):
            st.session_state.players = load_initial_players()
            st.success("איפוס בוצע!")
            st.rerun()

    # עמוד ראשי
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("👥 רשימת שחקנים")

        # סטטיסטיקות
        present_players = [p for p in st.session_state.players if p.present]
        total_players = len(st.session_state.players)
        present_count = len(present_players)
        avg_rating = sum(p.rating for p in present_players) / present_count if present_count > 0 else 0
        possible_teams = (present_count + 4) // 5

        st.markdown(f"""
        <div class="stats-container">
            <h3 style="color: #2c3e50;">📊 סטטיסטיקות</h3>
            <ul style="color: #2c3e50;">
                <li><strong>סה"כ שחקנים:</strong> {total_players}</li>
                <li><strong>שחקנים נוכחים:</strong> {present_count}</li>
                <li><strong>דירוג ממוצע (נוכחים):</strong> {avg_rating:.1f}</li>
                <li><strong>מספר קבוצות אפשריות:</strong> {possible_teams}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.subheader("בחר שחקנים נוכחים:")

        # רשימת שחקנים עם checkboxes
        cols = st.columns(3)
        for i, player in enumerate(st.session_state.players):
            with cols[i % 3]:
                current_status = player.present
                new_status = st.checkbox(
                    f"{player.name} ({player.rating}⭐)",
                    value=current_status,
                    key=f"player_{i}"
                )

                if new_status != current_status:
                    player.present = new_status

    with col2:
        st.header("⚽ חלוקת קבוצות")

        if present_count >= 5:
            if st.button("🎲 הגרל קבוצות!", type="primary", use_container_width=True):
                teams = balance_teams(present_players, possible_teams)
                st.session_state.teams = teams
                st.rerun()

            # הצגת תוצאות
            if 'teams' in st.session_state and st.session_state.teams:
                st.subheader("🏆 תוצאות החלוקה")

                total_avg = sum(sum(p.rating for p in team) for team in st.session_state.teams) / sum(len(team) for team in st.session_state.teams)
                st.info(f"דירוג ממוצע כללי: {total_avg:.2f}")

                team_colors = ['yellow', 'red', 'blue', 'black']

                for i, team in enumerate(st.session_state.teams, 1):
                    if team:
                        team_rating = sum(p.rating for p in team)
                        avg_rating = team_rating / len(team)
                        color_class = team_colors[(i-1) % len(team_colors)]

                        st.markdown(f"""
                        <div class="team-container team-{color_class}">
                            <h4>קבוצה {i} ({len(team)} שחקנים)</h4>
                            <p><strong>דירוג כולל:</strong> {team_rating:.1f} | <strong>ממוצע:</strong> {avg_rating:.2f}</p>
                            <ul>
                        """, unsafe_allow_html=True)

                        for player in team:
                            st.markdown(f"<li>{player.name} ({player.rating}⭐)</li>", unsafe_allow_html=True)

                        st.markdown("</ul></div>", unsafe_allow_html=True)

                # איזון הקבוצות
                if len(st.session_state.teams) > 1:
                    ratings = [sum(p.rating for p in team) / len(team) for team in st.session_state.teams if team]
                    max_diff = max(ratings) - min(ratings)
                    st.metric("איזון הקבוצות", f"{max_diff:.2f}",
                              help="ככל שנמוך יותר - מאוזן יותר")
        else:
            st.warning("נדרשים לפחות 5 שחקנים נוכחים ליצירת קבוצות!")

    # עריכת שחקן קיים
    st.header("✏️ עריכת שחקן קיים")

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_player = st.selectbox(
            "בחר שחקן לעריכה:",
            options=[p.name for p in st.session_state.players],
            index=0 if st.session_state.players else None
        )

    if selected_player:
        player_to_edit = next(p for p in st.session_state.players if p.name == selected_player)

        with col2:
            new_name = st.text_input("שם חדש:", value=player_to_edit.name, key="edit_name")

        with col3:
            new_rating = st.slider("דירוג חדש:", 1.0, 5.0, player_to_edit.rating, 0.5, key="edit_rating")

        col_update, col_delete = st.columns(2)

        with col_update:
            if st.button("🔄 עדכן שחקן", use_container_width=True):
                if new_name != player_to_edit.name:
                    if any(p.name == new_name for p in st.session_state.players if p != player_to_edit):
                        st.error("שחקן עם שם זה כבר קיים!")
                    else:
                        player_to_edit.name = new_name
                        player_to_edit.rating = new_rating
                        st.session_state.players.sort(key=lambda p: p.name)
                        st.success("השחקן עודכן בהצלחה!")
                        st.rerun()
                else:
                    player_to_edit.rating = new_rating
                    st.success("הדירוג עודכן בהצלחה!")
                    st.rerun()

        with col_delete:
            if st.button("🗑️ מחק שחקן", use_container_width=True, type="secondary"):
                st.session_state.players = [p for p in st.session_state.players if p.name != selected_player]
                st.success(f"השחקן {selected_player} נמחק!")
                st.rerun()

    # הוראות שימוש
    with st.expander("💡 הוראות שימוש"):
        st.markdown("""
        ### איך להשתמש באפליקציה:

        1. **הוספת שחקנים:** השתמש בסייד-בר השמאלי להוספת שחקנים חדשים
        2. **סימון נוכחות:** סמן ✅ ליד כל שחקן שנוכח היום
        3. **הגרלת קבוצות:** לחץ על "הגרל קבוצות" לחלוקה מאוזנת
        4. **עריכה:** השתמש בחלק התחתון לעריכת פרטי שחקנים
        5. **שמירה:** לחץ "שמור נתונים" לשמירת השינויים

        ### טיפים:
        - האלגוריתם מחלק את השחקנים לפי דירוג ליצירת קבוצות מאוזנות
        - ככל שמספר "איזון הקבוצות" נמוך יותר - החלוקה מאוזנת יותר
        - האפליקציה שומרת את הנתונים אוטומטית בכל פעולה
        """)

if __name__ == "__main__":
    main()