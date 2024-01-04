from fastapi import FastAPI, Body, Cookie
from fastapi.responses import FileResponse, HTMLResponse
from typing import Optional
from .webhtml import FrontEnd, WebState
from .database import fake_users_db
from .security import create_jwt_token, verify_jwt_token


class TheApp:
    def __init__(self):
        self.app = FastAPI()
        self.frontend = FrontEnd()

        @self.app.post("/login")
        async def login(credentials: dict = Body(...)):
            username = credentials.get('login')
            password = credentials.get('password')
            user = fake_users_db.get(username)
            print(f"{username=} {password=}")
            if user is None or user["password"] != password:
                html_content = self.frontend.get_content(state=WebState.LOGIN_FAILED)
                return HTMLResponse(content=html_content, status_code=401)

            # Create a JWT token with user information
            token_data = {"sub": username}
            token = create_jwt_token(token_data)

            # Set the token as a cookie in the response
            html_content = self.frontend.get_content(state=WebState.LOGGED)
            response = HTMLResponse(content=html_content, status_code=200)
            response.set_cookie(key="token", value=token)

            return response

        @self.app.get("/")
        async def read_root(token: Optional[str] = Cookie(None)):
            user_info = verify_jwt_token(token)
            if not user_info:
                html_content = self.frontend.get_content(state=WebState.NOT_LOGGED)
            else:
                html_content = self.frontend.get_content(state=WebState.LOGGED)
            return HTMLResponse(content=html_content, status_code=200)

        @self.app.get("/favicon.ico")
        async def get_favicon():
            return FileResponse(self.frontend.get_favicon())