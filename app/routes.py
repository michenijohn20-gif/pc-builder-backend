from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Component, Category, Build, GPU, RAM, build_components
from app.serializers import serialize_gpu, serialize_ram
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)
