from flask import Blueprint, request
from init import db
from models.user import User
from datetime import date
from flask_jwt_extended import get_jwt_identity, jwt_required


@releases_bp.route('/')
def get_all_releases():
    stmt = db.select(Release).order_by(Release.artist.title())
    releases = db.session.scalars(stmt)
    return releases_schema.dump(releases)

@releases_bp.route('/<int:id>')
def get_one_release(id):
    stmt = db.select(Release).filter_by(id=id)
    release = db.session.scalar(stmt)
    if release:
        return release_schema.dump(release)
    else:
        return {'error': f'Release not found with id {id}'}, 404