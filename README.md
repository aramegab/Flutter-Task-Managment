# Task Manager App

A task management app with a **Flutter** frontend and **FastAPI** backend. Users can view, add, delete, and mark tasks as completed. Tasks are stored in a SQLite database.

## Key Files

- **`lib/main.dart`**: Flutter app entry point, sets up `TaskProvider` and displays `TaskListScreen`.
- **`lib/models/task.dart`**: Defines `Task` model (`id`, `title`, `description`, `completed`) with JSON serialization.
- **`lib/providers/task_provider.dart`**: Manages task state, handles API calls for CRUD operations.
- **`lib/screens/task_list_screen.dart`**: Main UI screen, shows task list with add/delete/complete actions.
- **`lib/services/api_service.dart`**: Handles HTTP requests to FastAPI (GET, POST, PUT, DELETE).
- **`server/main.py`**: FastAPI server, defines API endpoints and SQLite database interactions.

## Setup and Run

### Prerequisites
- Flutter (2.12.0+): [Install](https://flutter.dev/docs/get-started/install)
- Python (3.8+): [Install](https://www.python.org/downloads/)
- Android emulator or device

### Backend (FastAPI)
1. Navigate to server:
   ```bash
   cd server
   ```

1. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

2. Run server:

   ```bash
   uvicorn main:app --reload
   ```

   - Server runs on `http://127.0.0.1:8000`.
   - Test: `curl http://127.0.0.1:8000/tasks/`

### Frontend (Flutter)

1. Navigate to project root:

   ```bash
   cd path/to/flutter_newproj
   ```

2. Install dependencies:

   ```bash
   flutter pub get
   ```

3. Ensure `lib/services/api_service.dart` uses `http://127.0.0.1:8000` (emulator) or machine IP (device).

4. Run app:

   ```bash
   flutter run
   ```

## Usage

- View tasks in the list.
- Add tasks via the Floating Action Button.
- Mark tasks as completed with checkboxes.
- Delete tasks with the delete icon.
- Refresh tasks with the AppBar button.

## Troubleshooting

- **No tasks displayed**:
  - Check `tasks.db`: `sqlite3 tasks.db "SELECT * FROM tasks;"`
  - Add test task: `curl -X POST "http://127.0.0.1:8000/tasks/" -H "Content-Type: application/json" -d '{"title":"Test Task","description":"Test","completed":false}'`
  - Verify API: `curl http://127.0.0.1:8000/tasks/`
- **Network errors**:
  - Ensure server is running and `baseUrl` is correct.
  - Check `<uses-permission android:name="android.permission.INTERNET" />` in `android/app/src/main/AndroidManifest.xml`.
- **Build issues**:
  - Run `flutter clean && flutter pub get`.
