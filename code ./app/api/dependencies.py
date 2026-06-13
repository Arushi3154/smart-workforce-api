from app.models.database import SessionLocal

def get_db():
    """
    Creates an independent database session for each request.
    Yields the session to the endpoint, then safely closes it afterward.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()