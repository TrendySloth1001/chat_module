import asyncio
import websockets
import uuid
import json

sessions = {}  # session_id: set of (websocket, user_id)
user_sessions = {}  # websocket: (session_id, user_id)

async def broadcast_presence(session_id):
    users = [user_id for ws, user_id in sessions.get(session_id, set())]
    msg = json.dumps({'type': 'presence', 'users': users})
    for ws, _ in sessions.get(session_id, set()):
        await ws.send(msg)

async def handler(websocket):
    session_id = None
    user_id = str(uuid.uuid4())
    try:
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'join':
                session_id = data['session_id']
                if session_id not in sessions:
                    sessions[session_id] = set()
                sessions[session_id].add((websocket, user_id))
                user_sessions[websocket] = (session_id, user_id)
                await broadcast_presence(session_id)
            elif data['type'] in ('edit', 'open_file') and session_id:
                # Broadcast to all other clients in the session
                for ws, _ in sessions[session_id]:
                    if ws != websocket:
                        await ws.send(json.dumps({**data, 'user_id': user_id}))
    except Exception:
        pass
    finally:
        if session_id:
            sessions[session_id] = {(ws, uid) for ws, uid in sessions[session_id] if ws != websocket}
            if not sessions[session_id]:
                del sessions[session_id]
            if websocket in user_sessions:
                del user_sessions[websocket]
            await broadcast_presence(session_id)

async def main():
    async with websockets.serve(handler, 'localhost', 8765):
        print('Collaboration server running on ws://localhost:8765')
        await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main()) 