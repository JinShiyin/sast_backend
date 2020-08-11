import time

from flask import session
from flask_socketio import (
    SocketIO,
    disconnect,
    join_room,
    leave_room,
    emit, Namespace
)
from flask import Flask, render_template, request

from config import Config
import eventlet

eventlet.monkey_patch(thread=False)

import logging

logger = logging.getLogger('gunicorn.error')

socketio = SocketIO(cors_allowed_origins="*")


@socketio.on('connect')
def connect():
    sid = request.sid
    print(f'Socket connection created with {sid}')


@socketio.on('disconnect')
def disconnect():
    sid = request.sid
    print(f'Socket disconnected from {sid}')


def synthesis_complete(body):
    """
    notify frontend that a stylization image is obtainable.
    :param body: {
            'content_id': content_id,
            'style_id': style_id,
            'stylization_id': stylization_id,
        }
    :return:
    """
    print(f'notify fronted synthesis completely with body: {body}')
    socketio.emit('onSynthesisCompleted', body, broadcast=True)


def synthesising(body):
    """
    notify frontend with current synthesis progress.
    The frontend mustn't fetching stylization image from backend if the image's status is 'SYNTHESISING'
    :param body: {
        'content_id': content_id,
        'style_id': style_id,
        'stylization_id': stylization_id,
        'current_update_steps': 100,
        'current_cost_time': 200,
        'percent': 0.35, # 1 represent 'COMPLETE',otherwise it is 'SYNTHESISING',
        'total_time': 10,
        'total_update_steps': 10,
    }
    :return:
    """
    print(f'notify fronted synthesis with body: {body}')
    socketio.emit('onSynthesising', body, broadcast=True)
