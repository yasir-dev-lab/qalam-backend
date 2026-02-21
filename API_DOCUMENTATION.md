# Qalam Backend API Documentation

Version: `0.1.0`
Base URL (local): `http://localhost:8000`
API Prefix: `/api`

This backend is a single-user note-taking API (no authentication).

## Tech Stack

- FastAPI
- SQLModel
- PostgreSQL

## Run the API

```powershell
Set-Location e:\Qalam\backend
& "C:/Program Files/Python312/python.exe" -m uvicorn app.main:app --reload
```

Open docs:
- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Data Models

### Tag

```json
{
  "id": 1,
  "name": "python",
  "color": "#3572A5"
}
```

Rules:
- `name`: required, 1-50 chars
- `color`: optional, max 20 chars
- Tag names must be unique (conflict returns `409`)

### Note

```json
{
  "id": 1,
  "title": "Hello Qalam",
  "body": "# Markdown content",
  "created_at": "2026-02-21T12:00:00Z",
  "updated_at": "2026-02-21T12:00:00Z",
  "tags": [
    {
      "id": 1,
      "name": "python",
      "color": "#3572A5"
    }
  ]
}
```

Rules:
- `title`: required, 1-255 chars
- `body`: optional string (Markdown supported)
- `created_at` and `updated_at` are server-generated

---

## Endpoints

## Root

### `GET /`
Returns a simple health-style welcome payload.

Response `200`:

```json
{
  "message": "Welcome to Qalam API",
  "docs": "/docs"
}
```

---

## Notes

### `GET /api/notes/`
List notes (newest by `updated_at` first).

Query params:
- `q` (optional): case-insensitive keyword search in `title` or `body`
- `tag_id` (optional): filter notes by attached tag id
- `offset` (optional, default `0`, min `0`)
- `limit` (optional, default `50`, min `1`, max `200`)

Response `200`: `NoteReadWithTags[]`

---

### `POST /api/notes/`
Create a note.

Request body:

```json
{
  "title": "My first note",
  "body": "# Heading\nSome markdown text"
}
```

Response `201`: `NoteReadWithTags`

---

### `GET /api/notes/{note_id}`
Get one note with all its tags.

Response:
- `200`: `NoteReadWithTags`
- `404`: note not found

---

### `PATCH /api/notes/{note_id}`
Partially update a note.

Request body (any subset):

```json
{
  "title": "Updated title",
  "body": "Updated markdown"
}
```

Response:
- `200`: updated `NoteReadWithTags`
- `404`: note not found

Notes:
- `updated_at` is automatically refreshed on every successful update.

---

### `DELETE /api/notes/{note_id}`
Delete a note.

Response:
- `204`: deleted
- `404`: note not found

---

### `POST /api/notes/{note_id}/tags/{tag_id}`
Attach an existing tag to a note.

Response:
- `200`: updated `NoteReadWithTags`
- `404`: note not found or tag not found
- `409`: tag is already attached to this note

---

### `DELETE /api/notes/{note_id}/tags/{tag_id}`
Detach a tag from a note (tag itself is not deleted).

Response:
- `200`: updated `NoteReadWithTags`
- `404`: note not found or tag is not attached to the note

---

## Tags

### `GET /api/tags/`
List all tags ordered by name.

Response `200`: `TagRead[]`

---

### `POST /api/tags/`
Create a tag.

Request body:

```json
{
  "name": "python",
  "color": "#3572A5"
}
```

Response:
- `201`: `TagRead`
- `409`: duplicate tag name

---

### `GET /api/tags/{tag_id}`
Get one tag and the notes it is attached to.

Response:
- `200`: `TagReadWithNotes`
- `404`: tag not found

---

### `PATCH /api/tags/{tag_id}`
Partially update tag fields.

Request body (any subset):

```json
{
  "name": "backend",
  "color": "#111827"
}
```

Response:
- `200`: updated `TagRead`
- `404`: tag not found
- `409`: duplicate tag name

---

### `DELETE /api/tags/{tag_id}`
Delete a tag and remove it from linked notes.

Response:
- `204`: deleted
- `404`: tag not found

---

## Error Format

For handled errors (`404`, `409`, etc.), FastAPI returns:

```json
{
  "detail": "Error message"
}
```

Validation failures return `422` with FastAPI/Pydantic validation details.

---

## Quick cURL Examples

Create tag:

```bash
curl -X POST "http://localhost:8000/api/tags/" \
  -H "Content-Type: application/json" \
  -d '{"name":"python","color":"#3572A5"}'
```

Create note:

```bash
curl -X POST "http://localhost:8000/api/notes/" \
  -H "Content-Type: application/json" \
  -d '{"title":"Hello","body":"# Markdown"}'
```

Attach tag to note:

```bash
curl -X POST "http://localhost:8000/api/notes/1/tags/1"
```

Search notes:

```bash
curl "http://localhost:8000/api/notes/?q=hello&limit=20"
```

Filter notes by tag:

```bash
curl "http://localhost:8000/api/notes/?tag_id=1"
```
