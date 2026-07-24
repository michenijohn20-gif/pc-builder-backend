from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Component, Category, Build, GPU, RAM, build_components
from app.serializers import serialize_gpu, serialize_ram
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

api_bp = Blueprint('api', __name__)

def get_owned_build_or_403(build_id, user_id):
    build = Build.query.get_or_404(build_id)
    if build.user_id != user_id:
        return None
    return build

#  AUTHENTICATION ENDPOINTS 

@api_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
        
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

@api_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()
    
    if user is None or not user.check_password(data.get('password')):
        return jsonify({'error': 'Invalid email or password'}), 401
        
    access_token = create_access_token(identity=str(user.id))
    return jsonify({'access_token': access_token, 'username': user.username}), 200

@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def me():
    current_user_id = int(get_jwt_identity())
    user = User.query.get_or_404(current_user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email
    }), 200

# COMPONENTS ENDPOINTS 

@api_bp.route('/components', methods=['GET'])
def get_components():
    page = request.args.get('page', type=int)
    per_page = request.args.get('per_page', type=int)
    query = Component.query.order_by(Component.id)

    if page or per_page:
        page = page or 1
        per_page = per_page or 12
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        components = pagination.items
    else:
        components = query.all()

    output = []
    for c in components:
        output.append({
            'id': c.id,
            'name': c.name,
            'brand': c.brand,
            'price': c.price,
            'socket': c.socket,
            'image_url': c.image_url,
            'category': c.category.name if c.category else None
        })

    if page or per_page:
        return jsonify({
            'items': output,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        }), 200

    return jsonify(output), 200

@api_bp.route('/components/<int:id>', methods=['GET'])
def get_component(id):
    c = Component.query.get_or_404(id)
    return jsonify({
        'id': c.id,
        'name': c.name,
        'brand': c.brand,
        'price': c.price,
        'socket': c.socket,
        'image_url': c.image_url,
        'category': c.category.name if c.category else None
    }), 200

# GPU ENDPOINTS

@api_bp.route('/gpus', methods=['GET'])
def get_gpus():
    return jsonify([serialize_gpu(gpu) for gpu in GPU.query.order_by(GPU.id).all()]), 200


@api_bp.route('/gpus/<int:id>', methods=['GET'])
def get_gpu(id):
    gpu = GPU.query.get_or_404(id)
    return jsonify(serialize_gpu(gpu)), 200


@api_bp.route('/gpus', methods=['POST'])
@jwt_required()
def create_gpu():
    data = request.get_json() or {}
    if not all(field in data for field in ('name', 'brand', 'price', 'vram')):
        return jsonify({'error': 'Missing required fields'}), 400

    gpu = GPU(
        name=data['name'],
        brand=data['brand'],
        price=data['price'],
        vram=data['vram'],
        specs=data.get('specs') or {},
        image_url=data.get('image_url')
    )
    db.session.add(gpu)
    db.session.commit()
    return jsonify(serialize_gpu(gpu)), 201


@api_bp.route('/gpus/<int:id>', methods=['PUT'])
@jwt_required()
def update_gpu(id):
    gpu = GPU.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ('name', 'brand', 'price', 'vram'):
        if field in data:
            setattr(gpu, field, data[field])
    if 'specs' in data:
        gpu.specs = data['specs'] or {}
    if 'image_url' in data:
        gpu.image_url = data['image_url']
    db.session.commit()
    return jsonify(serialize_gpu(gpu)), 200


@api_bp.route('/gpus/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_gpu(id):
    gpu = GPU.query.get_or_404(id)
    db.session.delete(gpu)
    db.session.commit()
    return jsonify({'message': 'GPU deleted successfully'}), 200

# RAM ENDPOINTS

@api_bp.route('/rams', methods=['GET'])
def get_rams():
    return jsonify([serialize_ram(ram) for ram in RAM.query.order_by(RAM.id).all()]), 200


@api_bp.route('/rams/<int:id>', methods=['GET'])
def get_ram(id):
    ram = RAM.query.get_or_404(id)
    return jsonify(serialize_ram(ram)), 200


@api_bp.route('/rams', methods=['POST'])
@jwt_required()
def create_ram():
    data = request.get_json() or {}
    if not all(field in data for field in ('name', 'brand', 'price', 'capacity')):
        return jsonify({'error': 'Missing required fields'}), 400

    ram = RAM(
        name=data['name'],
        brand=data['brand'],
        price=data['price'],
        capacity=data['capacity'],
        speed=data.get('speed'),
        specs=data.get('specs') or {},
        image_url=data.get('image_url')
    )
    db.session.add(ram)
    db.session.commit()
    return jsonify(serialize_ram(ram)), 201


@api_bp.route('/rams/<int:id>', methods=['PUT'])
@jwt_required()
def update_ram(id):
    ram = RAM.query.get_or_404(id)
    data = request.get_json() or {}
    for field in ('name', 'brand', 'price', 'capacity', 'speed'):
        if field in data:
            setattr(ram, field, data[field])
    if 'specs' in data:
        ram.specs = data['specs'] or {}
    if 'image_url' in data:
        ram.image_url = data['image_url']
    db.session.commit()
    return jsonify(serialize_ram(ram)), 200


@api_bp.route('/rams/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ram(id):
    ram = RAM.query.get_or_404(id)
    db.session.delete(ram)
    db.session.commit()
    return jsonify({'message': 'RAM deleted successfully'}), 200

# BUILD MANAGEMENT ENDPOINTS 

# 1. Create a new build
@api_bp.route('/builds', methods=['POST'])
@jwt_required()
def create_build():
    current_user_id = get_jwt_identity()
    data = request.get_json() or {}
    
    if 'name' not in data:
        return jsonify({'error': 'Build name is required'}), 400
        
    new_build = Build(
        user_id=int(current_user_id),
        name=data['name'],
        total_price=0.0
    )
    db.session.add(new_build)
    db.session.commit()
    
    return jsonify({
        'message': 'Build created successfully',
        'build': {'id': new_build.id, 'name': new_build.name}
    }), 201

@api_bp.route('/builds/<int:build_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_build(build_id):
    current_user_id = int(get_jwt_identity())
    build = get_owned_build_or_403(build_id, current_user_id)
    if build is None:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json() or {}
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Build name is required'}), 400

    build.name = name
    db.session.commit()
    return jsonify({
        'message': 'Build updated successfully',
        'build': {
            'id': build.id,
            'name': build.name,
            'total_price': build.total_price
        }
    }), 200


# 2b. Remove a component from a build
@api_bp.route('/builds/<int:build_id>/remove/<int:component_id>', methods=['DELETE'])
@jwt_required()
def remove_component_from_build(build_id, component_id):
    current_user_id = int(get_jwt_identity())
    build = get_owned_build_or_403(build_id, current_user_id)
    if build is None:
        return jsonify({'error': 'Forbidden'}), 403

    component = Component.query.get_or_404(component_id)

    rows = db.session.execute(
        select(build_components.c.id).where(
            build_components.c.build_id == build_id,
            build_components.c.component_id == component_id
        )
    ).fetchall()

    if not rows:
        return jsonify({'error': 'Component not found in build'}), 404

    removed_count = len(rows)
    db.session.execute(
        build_components.delete().where(
            build_components.c.build_id == build_id,
            build_components.c.component_id == component_id
        )
    )

    current_total = float(build.total_price or 0.0)
    comp_price = float(component.price or 0.0)
    build.total_price = max(current_total - comp_price * removed_count, 0.0)

    db.session.commit()

    return jsonify({
        'message': f'Removed {removed_count} x {component.name} from build successfully',
        'removed_count': removed_count,
        'total_price': build.total_price
    }), 200

# 2. Add a component to a build
@api_bp.route('/builds/<int:build_id>/add/<int:component_id>', methods=['POST'])
@jwt_required()
def add_component_to_build(build_id, component_id):
    current_user_id = int(get_jwt_identity())
    build = get_owned_build_or_403(build_id, current_user_id)
    if build is None:
        return jsonify({'error': 'Forbidden'}), 403
    component = Component.query.get_or_404(component_id)
    
    # Optional compatibility check (e.g., matching CPU and Motherboard socket)
    if component.category.name == "Motherboard" or component.category.name == "CPU":
        for existing_comp in build.components:
            if existing_comp.category.name in ["CPU", "Motherboard"] and existing_comp.socket != component.socket:
                return jsonify({
                    'error': f"Incompatible socket! {component.name} ({component.socket}) does not match {existing_comp.name} ({existing_comp.socket})."
                }), 400

    build.components.append(component)
    build.total_price += component.price
    db.session.commit()
    
    return jsonify({'message': f'Added {component.name} to build successfully', 'total_price': build.total_price}), 200

# 3. Get all builds belonging to the logged-in user
@api_bp.route('/builds', methods=['GET'])
@jwt_required()
def get_user_builds():
    current_user_id = int(get_jwt_identity())
    user_builds = Build.query.filter_by(user_id=int(current_user_id)).all()
    
    output = []
    for b in user_builds:
        output.append({
            'id': b.id,
            'name': b.name,
            'total_price': b.total_price,
            'created_at': b.created_at.strftime('%Y-%m-%d'),
            'components': [{'id': c.id, 'name': c.name, 'price': c.price} for c in b.components]
        })
    return jsonify(output), 200

# 4. Delete a build
@api_bp.route('/builds/<int:build_id>', methods=['DELETE'])
@jwt_required()
def delete_build(build_id):
    current_user_id = int(get_jwt_identity())
    build = get_owned_build_or_403(build_id, current_user_id)
    if build is None:
        return jsonify({'error': 'Forbidden'}), 403
    
    db.session.delete(build)
    db.session.commit()
    return jsonify({'message': 'Build deleted successfully'}), 200
