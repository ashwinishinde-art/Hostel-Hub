"""
Real-time WebSocket server for instant updates across all connected devices
Uses Flask-SocketIO for WebSocket communication
"""

from flask_socketio import SocketIO, emit, broadcast, join_room, leave_room
import json
from datetime import datetime

def init_socketio(app):
    """Initialize SocketIO for real-time updates"""
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')
    
    # Store connected clients
    connected_clients = {
        'gallery': set(),
        'complaints': set(),
        'notices': set(),
        'fees': set(),
        'visitors': set(),
        'students': set(),
        'rooms': set()
    }
    
    @socketio.on('connect')
    def handle_connect():
        """Handle client connection"""
        print(f'Client connected: {request.sid}')
        emit('connection_response', {'data': 'Connected to real-time server'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle client disconnection"""
        print(f'Client disconnected: {request.sid}')
        # Remove from all rooms
        for room in connected_clients.values():
            room.discard(request.sid)
    
    @socketio.on('subscribe')
    def handle_subscribe(data):
        """Subscribe to updates for specific feature"""
        feature = data.get('feature', 'gallery')
        if feature in connected_clients:
            connected_clients[feature].add(request.sid)
            join_room(feature)
            print(f'Client {request.sid} subscribed to {feature}')
            emit('subscribed', {'feature': feature, 'timestamp': datetime.now().isoformat()})
    
    @socketio.on('unsubscribe')
    def handle_unsubscribe(data):
        """Unsubscribe from updates"""
        feature = data.get('feature', 'gallery')
        if feature in connected_clients:
            connected_clients[feature].discard(request.sid)
            leave_room(feature)
            print(f'Client {request.sid} unsubscribed from {feature}')
    
    return socketio, connected_clients


def broadcast_update(socketio, feature, action, data):
    """Broadcast update to all connected clients for a feature"""
    message = {
        'action': action,
        'data': data,
        'timestamp': datetime.now().isoformat(),
        'feature': feature
    }
    
    print(f'Broadcasting {action} to {feature}: {message}')
    socketio.emit('update', message, room=feature)


def broadcast_gallery_update(socketio, action, image_data):
    """Broadcast gallery updates"""
    broadcast_update(socketio, 'gallery', action, image_data)


def broadcast_complaint_update(socketio, action, complaint_data):
    """Broadcast complaint updates"""
    broadcast_update(socketio, 'complaints', action, complaint_data)


def broadcast_notice_update(socketio, action, notice_data):
    """Broadcast notice updates"""
    broadcast_update(socketio, 'notices', action, notice_data)


def broadcast_room_update(socketio, action, room_data):
    """Broadcast room updates"""
    broadcast_update(socketio, 'rooms', action, room_data)


def broadcast_student_update(socketio, action, student_data):
    """Broadcast student updates"""
    broadcast_update(socketio, 'students', action, student_data)


def broadcast_fee_update(socketio, action, fee_data):
    """Broadcast fee updates"""
    broadcast_update(socketio, 'fees', action, fee_data)


def broadcast_visitor_update(socketio, action, visitor_data):
    """Broadcast visitor updates"""
    broadcast_update(socketio, 'visitors', action, visitor_data)
