import json
import time
from datetime import date
from pathlib import Path


LOG_FILE = Path("focus_log.json")


def load_sessions():
	if not LOG_FILE.exists():
		return []

	with LOG_FILE.open("r", encoding="utf-8") as file:
		return json.load(file)


def save_sessions(sessions):
	with LOG_FILE.open("w", encoding="utf-8") as file:
		json.dump(sessions, file, indent=2)


sessions = load_sessions()


def run_session():
	name = input("Session name: ")
	start_time = time.monotonic()
	input("Press Enter to stop the session.")
	minutes = round((time.monotonic() - start_time) / 60, 1)

	sessions.append({
		"name": name,
		"date": date.today().isoformat(),
		"minutes": minutes,
	})
	save_sessions(sessions)


def show_today_summary():
	today = date.today().isoformat()
	todays_sessions = [session for session in sessions if session["date"] == today]

	if not todays_sessions:
		print("No focus sessions logged today.")
		return

	sessions_by_name = {}
	for session in todays_sessions:
		name = session["name"]
		sessions_by_name[name] = sessions_by_name.get(name, 0) + session["minutes"]

	print("Today's sessions:")
	for name, minutes in sessions_by_name.items():
		print(f"{name}: {round(minutes, 1)} minutes")
	print(f"Total: {round(sum(session['minutes'] for session in todays_sessions), 1)} minutes")


def main():
	while True:
		print("\n1. Start a focus session")
		print("2. Show today's summary")
		print("3. Quit")
		choice = input("Choose an option: ")

		if choice == "1":
			run_session()
		elif choice == "2":
			show_today_summary()
		elif choice == "3":
			break
		else:
			print("Invalid choice.")


if __name__ == "__main__":
	main()

