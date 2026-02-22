from sqlalchemy.orm import Session
from app.models.notification_model import Notification


def create_notification(db: Session, seller_id: int, event: str, data: dict | None = None) -> Notification:
    notif = Notification(
        seller_id=seller_id,
        event=event,
        data=data,
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif


def get_notifications(db: Session, seller_id: int, unread_only: bool = False) -> list[Notification]:
    query = db.query(Notification).filter(Notification.seller_id == seller_id)
    if unread_only:
        query = query.filter(Notification.read == False)
    return query.order_by(Notification.created_at.desc()).all()


def mark_notification_as_read(db: Session, notif_id: int) -> None:
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if notif:
        notif.read = True
        db.commit()
