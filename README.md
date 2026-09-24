# FastAPI Assessment 2

This project contains two FastAPI applications developed as part of the FastAPI Application-Based Practical Assessment.

## Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Pydantic
- Uvicorn
- Swagger UI

---

# Task 1: Campus Lost & Found API

This API is used to manage lost and found items on campus.

## Item Fields

- `id` - Unique item ID
- `title` - Name/title of the item
- `description` - Description of the item
- `category` - Category of the item
- `location` - Location where the item was lost/found
- `reported_by` - Person who reported the item
- `status` - Lost, Found, or Returned

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/items` | Create a new item |
| GET | `/items` | Get all items |
| GET | `/items/{item_id}` | Get item by ID |
| PUT | `/items/{item_id}` | Update an item |
| DELETE | `/items/{item_id}` | Delete an item |
| GET | `/items/status/{status}` | Filter items by status |
| GET | `/items/category/{category}` | Filter items by category |

## Validation

- Title cannot be empty.
- Description must contain at least 3 characters.
- Required fields are validated.
- Status can only be `Lost`, `Found`, or `Returned`.
- If an item does not exist, the API returns a 404 error.
- Invalid input returns a validation error.

## Database

Task 1 uses SQLite with SQLModel.

Database file:

`lost_found.db`

---

# Task 2: Campus Event Seat Reservation API

This API is used to create campus events and manage student seat reservations.

## Event Fields

- `id` - Unique event ID
- `title` - Event title
- `venue` - Event venue
- `capacity` - Maximum number of seats
- `organizer` - Event organizer
- `status` - Open or Closed

## Reservation Fields

- `id` - Unique reservation ID
- `event_id` - ID of the event
- `student_name` - Student name
- `roll_number` - Student roll number
- `email` - Student email

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create an event |
| GET | `/events` | Get all events |
| GET | `/events/{event_id}` | Get event by ID |
| PUT | `/events/{event_id}` | Update an event |
| DELETE | `/events/{event_id}` | Delete an event |
| POST | `/events/{event_id}/reserve` | Reserve a seat |
| GET | `/events/{event_id}/reservations` | Get reservations of an event |
| DELETE | `/reservations/{reservation_id}` | Cancel a reservation |
| GET | `/events/{event_id}/availability` | Check seat availability |

## Reservation Logic

The API checks the following conditions before creating a reservation:

1. The event must exist.
2. The event must be Open.
3. The number of reservations is counted.
4. A new reservation is rejected if the event is full.
5. Event capacity must be greater than 0.
6. Student name and roll number cannot be empty.
7. Email must be in a valid email format.

This prevents overbooking and reservations for closed events.

## Database

Task 2 uses SQLite with SQLModel.

Database file:

`events.db`

---

# Project Structure

```text
FastAPI-Assessment-2/
│
├── Task1_LostFound/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── main.py
│
├── Task2_EventReservation/
│   ├── __init__.py
│   ├── models.py
│   ├── database.py
│   ├── schemas.py
│   └── main.py
│
├── screenshots/
│
├── requirements.txt
├── .gitignore
└── README.md