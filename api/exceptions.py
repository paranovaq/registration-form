from fastapi import HTTPException

same_email_user = HTTPException(status_code=400, detail="This email is already registered")

same_telegram_user = HTTPException(status_code=400, detail="This telegram is already registered")

null_email_user = HTTPException(status_code=400, detail="There is no such email user")

null_telegram_user = HTTPException(status_code=400, detail="There are no such telegram user")