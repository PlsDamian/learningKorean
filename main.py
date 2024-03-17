import sqlite3
from datetime import datetime, timedelta


#  create db
def create_database():
    connection = sqlite3.connect('korean_progress.db')
    c = connection.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS progress
                (date TEXT PRIMARY KEY, phase INTEGER, completed INTEGER)''')

    connection.commit()
    connection.close()


#  mark progress
def mark_progress(date, phase, completed):
    connection = sqlite3.connect('korean_progress.db')
    c = connection.cursor()
    c.execute('''INSERT OR REPLACE INTO progress (date, phase, completed)
                VALUES (?, ?, ?)''', (date, phase, completed))

    connection.commit()
    connection.close()


#  display progress
def display_progress():
    connection = sqlite3.connect('korean_progress.db')
    c = connection.cursor()
    c.execute('''SELECT * FROM progress''')
    rows = c.fetchall()
    print("Date\t\tPhase\tCompleted")

    for row in rows:
        print(f"{row[0]}\t{row[1]}\t{row[2]}")
    connection.close()


tasks = {
    1: "Learn Hangul (Korean alphabet) and basic greetings and expressions.",
    2: "Learn 10 new words and practice forming simple sentences using new vocabulary.",
    3: "Study basic Korean grammar rules and practice constructing sentences with different grammar patterns.",
    4: "Listen to Korean podcasts, music, or watch short videos to understand spoken language. Speak aloud and mimic "
       "native speakers.",
    5: "Read Korean children's books, blogs, or news articles. Work on comprehension exercises.",
    6: "Practice writing short paragraphs or diary entries in Korean. Review writing focusing on grammar, vocabulary, "
       "and sentence structure."
}


def show_task_schedule():
    start_date = datetime(2024, 3, 17)
    current_date = datetime.today()
    current_phase = (current_date - start_date).days // 7 + 1

    print("Task Schedule: ")
    for phase, task in tasks.items():
        phase_start_date = start_date + timedelta(days=(phase - 1) * 7)
        phase_end_date = phase_start_date + timedelta(days=6)
        print(
            f"Phase {phase}: {task} (from {phase_start_date.strftime('%Y-%m-%d')} to "
            f"{phase_end_date.strftime('%Y-%m-d')})")

        #  calculate progress
        total_days = (phase_end_date - phase_start_date).days + 1
        completed_days = 0
        connection = sqlite3.connect('korean_progress.db')
        c = connection.cursor()
        c.execute('''SELECT completed FROM progress WHERE phase=?''', (phase,))
        rows = c.fetchall()

        for row in rows:
            completed_days += row[0]
        connection.close()

        progress_percent = (completed_days / total_days) * 100
        print(f"Progress: {progress_percent: .2f}%\n")

        if phase == current_phase:
            print(">> Current Phase <<")


def main():
    create_database()
    while True:
        print("\nWhat would you like to do?")
        print("1. Mark progress for today")
        print("2. View progress")
        print("3. Show task schedule")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            today = datetime.today().strftime('%Y-%m-%d')
            phase = (datetime.today() - datetime(2024, 3, 17)).days // 7 + 1
            completed = input(f"Did you complete tasks for Phase {phase} today? (yes/no): ").lower()

            if completed == 'yes':
                mark_progress(today, phase, 1)
            elif completed == 'no':
                mark_progress(today, phase, 0)
            else:
                print("Invalid entry")
        elif choice == '2':
            display_progress()
        elif choice == '3':
            show_task_schedule()
        elif choice == '4':
            print("Exiting program..")
            break
        else:
            print("Invalid entry")


if __name__ == '__main__':
    main()
