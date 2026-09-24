from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from .database import engine, create_tables
from .models import Event, EventStatus, Reservation
from .schemas import EventCreate, ReservationCreate


app = FastAPI(title="Campus Event Seat Reservation API")


@app.on_event("startup")
def startup():
    create_tables()


@app.post("/events")
def create_event(event_data: EventCreate):
    if event_data.capacity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Capacity must be greater than 0"
        )

    event = Event(**event_data.model_dump())

    with Session(engine) as session:
        session.add(event)
        session.commit()
        session.refresh(event)

        return event


@app.get("/events")
def get_events():
    with Session(engine) as session:
        events = session.exec(select(Event)).all()

        return events


@app.get("/events/{event_id}")
def get_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        return event


@app.put("/events/{event_id}")
def update_event(event_id: int, event_data: EventCreate):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        updated_data = event_data.model_dump()

        for key, value in updated_data.items():
            setattr(event, key, value)

        session.add(event)
        session.commit()
        session.refresh(event)

        return event


@app.delete("/events/{event_id}")
def delete_event(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        reservations = session.exec(
            select(Reservation).where(
                Reservation.event_id == event_id
            )
        ).all()

        for reservation in reservations:
            session.delete(reservation)

        session.delete(event)
        session.commit()

        return {"message": "Event deleted successfully"}


@app.post("/events/{event_id}/reserve")
def create_reservation(
    event_id: int,
    reservation_data: ReservationCreate
):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        if event.status == EventStatus.Closed:
            raise HTTPException(
                status_code=400,
                detail="Event is closed"
            )

        reservations = session.exec(
            select(Reservation).where(
                Reservation.event_id == event_id
            )
        ).all()

        booked_seats = len(reservations)

        if booked_seats >= event.capacity:
            raise HTTPException(
                status_code=400,
                detail="No seats available"
            )

        reservation = Reservation(
            event_id=event_id,
            **reservation_data.model_dump()
        )

        session.add(reservation)
        session.commit()
        session.refresh(reservation)

        return reservation


@app.get("/events/{event_id}/reservations")
def get_reservations(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        reservations = session.exec(
            select(Reservation).where(
                Reservation.event_id == event_id
            )
        ).all()

        return reservations


@app.delete("/reservations/{reservation_id}")
def delete_reservation(reservation_id: int):
    with Session(engine) as session:
        reservation = session.get(
            Reservation,
            reservation_id
        )

        if not reservation:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )

        session.delete(reservation)
        session.commit()

        return {"message": "Reservation cancelled successfully"}


@app.get("/events/{event_id}/availability")
def get_availability(event_id: int):
    with Session(engine) as session:
        event = session.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=404,
                detail="Event not found"
            )

        reservations = session.exec(
            select(Reservation).where(
                Reservation.event_id == event_id
            )
        ).all()

        booked_seats = len(reservations)
        remaining_seats = event.capacity - booked_seats

        return {
            "event_id": event.id,
            "capacity": event.capacity,
            "booked_seats": booked_seats,
            "remaining_seats": remaining_seats,
            "status": event.status
        }