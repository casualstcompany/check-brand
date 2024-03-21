from http import HTTPStatus

from api.v1.base import BaseAPI
from api.v1.response_code import get_error_response
from api.v1.serialization.user import user_image_schema, user_profile_schema, user_email_confirm
from api.v1.swag import user as swag
from config.utils import session_scope
from flasgger import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import Profile
from services.user import user_service
from services.email import email_service
from utils.check_allowed import check_image_to_allowed
from werkzeug.exceptions import RequestEntityTooLarge
from marshmallow.exceptions import ValidationError

user = Blueprint("user_api", __name__)


@user.route("/profile/my/add_image", methods=("POST",))
@jwt_required()
@swag_from(swag.add_user)
def add_image():
    try:
        image = request.files.get("image")
    except RequestEntityTooLarge:
        return get_error_response.error(
            "The data value transmitted exceeds the capacity limit.",
            status_code=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
        )
    if not image:
        return get_error_response.error_400({"image": ["required field"]})

    if not check_image_to_allowed(image.filename):
        return get_error_response.error_400(
            {"image": ["invalid image extension"]}
        )

    if len(image.filename) > 50:
        return get_error_response.error_400(
            {
                "image": [
                    "The file name is too long. Valid value: 100 characters."
                ]
            }
        )
    profile = user_service.add_image(image)

    return jsonify(user_image_schema.dump(profile)), HTTPStatus.OK


class ProfileView(BaseAPI):
    schema = user_profile_schema
    service = user_service

    def get_object(self):
        public_address = get_jwt_identity()
        user = self.service.get_profile_by_public_address(public_address)
        if not user:
            return self.error_500()
        return user

    @jwt_required()
    @swag_from(swag.my_profile)
    def get(self):
        model = self.get_object()
        return jsonify(self.schema.dump(model))

    @jwt_required()
    @swag_from(swag.my_profile_update)
    def put(self):
        data = self.get_data()
        if self.data_validation(data):
            model = self.get_object()

            with session_scope() as session:
                self.schema.load(data, instance=model, session=session)
            
            if model.email is not None and model.email_verified is None and data.get("email") is not None:
                email_service.send_email_confirm(
                    to=[model.email,], otp_code = model.email_otp
                    )

            return jsonify(self.schema.dump(model))


profile_view = ProfileView.as_view("user_api")
user.add_url_rule(
    "/profile/my", view_func=profile_view, methods=["GET", "PUT"]
)


@user.route("/profile/<public_address>", methods=("GET",))
@swag_from(swag.profile)
def get_user_profile(public_address):
    public_address = public_address.lower()
    if profile := Profile.query.filter_by(
        public_address=public_address
    ).first():
        return jsonify(user_profile_schema.dump(profile)), HTTPStatus.OK
    return get_error_response.error_404()

@user.route("/profile/confirm_email/<otp_code>", methods=("GET",))
@jwt_required(refresh=False)
@swag_from(swag.confirm_email)
def confirm_email_user(otp_code):

    try:
        otp_code = int(otp_code)
    except ValueError:
        return get_error_response.error_404()
    
    public_address = get_jwt_identity()
    public_address = public_address.lower()
    
    if profile := Profile.query.filter_by(
        public_address=public_address, 
        email_otp=otp_code
    ).first():
        data = {"email_verified": True, "email_otp": otp_code}
        
        with session_scope() as session:
            try:
                user_email_confirm.load(
                data, 
                instance=profile, 
                session=session
                )
            except ValidationError as e:
                return get_error_response.error_400(e.messages)

        return jsonify({"status": "success"}), HTTPStatus.OK
    return get_error_response.error_404()
