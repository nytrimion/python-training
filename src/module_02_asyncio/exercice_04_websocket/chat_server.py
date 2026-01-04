"""
Exercise 04: Mini-Chat WebSocket Server.

This module implements a simple chat server using WebSockets.
Multiple clients can connect and broadcast messages to each other.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path

import aiofiles
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI(title="Mini Chat WebSocket")


# --- Connection Manager ---


@dataclass
class ConnectionManager:
    """
    Manages WebSocket connections and message broadcasting.

    Attributes:
        active_connections: Dict mapping username to their WebSocket connection
    """

    active_connections: dict[str, WebSocket] = field(default_factory=dict)

    async def connect(self, websocket: WebSocket, username: str) -> bool:
        """
        Accept a new WebSocket connection.

        Args:
            websocket: The WebSocket connection to accept
            username: The username for this connection

        Returns:
            True if connection accepted, False if username already taken
        """
        if username in self.active_connections:
            return False

        await websocket.accept()
        self.active_connections[username] = websocket
        return True

    def disconnect(self, username: str) -> None:
        """Remove a connection from the manager."""
        if username in self.active_connections:
            del self.active_connections[username]

    def get_users(self) -> list[str]:
        """Return list of connected usernames."""
        return list(self.active_connections.keys())

    async def broadcast(self, message: str, exclude_user: str | None = None) -> None:
        """
        Send a message to all connected clients.

        Args:
            message: The message to broadcast
            exclude_user: Optional username to exclude from broadcast
        """
        for username, websocket in list(self.active_connections.items()):
            if username == exclude_user:
                continue
            try:
                await websocket.send_text(message)
            except WebSocketDisconnect:
                print(f"[broadcast] Client {username} disconnected")
                self.disconnect(username)
            except Exception:
                print(f"[broadcast] Failed to send message to client {username}")


# --- Simple View Manager ---


@dataclass
class SimpleViewManager:
    """
    Manages simple view contents.

    Attributes:
        views: Dict mapping view names to their content
    """

    views: dict[str, str] = field(default_factory=dict)

    async def render(self, name: str) -> str:
        """
        Provides a view content by its name, loaded in internal cache.

        Args:
            name: The view name

        Returns:
            The view's content
        """
        if name not in self.views:
            path = Path(__file__).parent / f"{name}.html"

            if not path.exists():
                raise FileNotFoundError(f"Template '{name}' not found")

            async with aiofiles.open(path) as file:
                self.views[name] = await file.read()

        return self.views[name]


# Global connection manager
connection_manager = ConnectionManager()
# Global view manager
view_manager = SimpleViewManager()


@app.get("/")
async def get_client() -> HTMLResponse:
    """Serve the HTML chat client."""
    return HTMLResponse(await view_manager.render("chat-client"))


# --- WebSocket Endpoint ---


@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str) -> None:
    """
    WebSocket endpoint for chat communication.

    Args:
        websocket: The WebSocket connection
        username: The username from the URL path
    """
    try:
        if not await connection_manager.connect(websocket, username):
            await websocket.close(4000, "Username already taken")
            return
    except WebSocketDisconnect:
        return

    await broadcast_system_notification(f"{username} joined the chat")
    await broadcast_users_list()
    try:
        while True:
            message = await websocket.receive_text()
            await broadcast_user_message(username, message)
    finally:
        connection_manager.disconnect(username)
        await broadcast_system_notification(f"{username} left the chat")
        await broadcast_users_list()


async def broadcast_system_notification(content: str) -> None:
    message = {
        "type": "system",
        "content": content,
    }
    await connection_manager.broadcast(json.dumps(message))


async def broadcast_user_message(username: str, content: str) -> None:
    message = {
        "type": "message",
        "username": username,
        "content": content,
    }
    await connection_manager.broadcast(json.dumps(message))


async def broadcast_users_list() -> None:
    message = {
        "type": "users",
        "users": connection_manager.get_users(),
    }
    await connection_manager.broadcast(json.dumps(message))


# --- Run instructions ---
# uvicorn chat_server:app --reload
# Open http://localhost:8000 in multiple browser tabs to test
