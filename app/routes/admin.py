"""Admin Blueprint for managing admin views."""
from flask import render_template, current_app, send_from_directory, jsonify
from flask_smorest import Blueprint
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
def admin_index():
    """
    Serves the admin menu page.
    """
    return render_template('admin_menu.html')

@admin_bp.route('/city-graph', methods=["GET"])
@admin_bp.response(200, {"message": {"type": "string"}}, description="City graph is correctly generated.")
@admin_bp.response(503, {"message": {"type": "string"}}, description="City graph is not correctly generated.")
def serve_city_graph():
    """
    Serves the city graph html file.
    """
    graph_path = os.path.join(current_app.root_path, 'static', 'city_graph.html')
    if os.path.exists(graph_path):
        return send_from_directory(os.path.dirname(graph_path), os.path.basename(graph_path))
    else:
        return jsonify({"message": "City graph not found"}), 503

@admin_bp.route('/cities', methods=['GET'])
def admin_cities():
    """
    Serves the cities management view.
    """
    return render_template('cities.html')

@admin_bp.route('/streets', methods=['GET'])
def admin_streets():
    """
    Serves the streets management view.
    """
    return render_template('streets.html')