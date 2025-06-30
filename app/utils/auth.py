from fastapi import Request, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..database.models import Session as SessionModel, User
from ..utils.date_utils import get_current_date

def get_current_user(request: Request, db: Session) -> User | None:
    """Получает пользователя из куки session_id с проверкой срока действия."""
    session_id = request.cookies.get("session_id")
    if not session_id:
        return None
    
    # Ищем сессию вместе с пользователем
    db_session = (
        db.query(SessionModel)
        .options(joinedload(SessionModel.user))  # Жадная загрузка
        .filter(SessionModel.session_id == session_id)
        .first()
    )
    
    if not db_session:
        return None
    
    # Проверяем, не истекла ли сессия
    current_timestamp = get_current_date()[1]
    if db_session.expires_at < current_timestamp:
        db.delete(db_session)
        db.commit()
        return None
    
    return db_session.user