import frappe
from frappe import _


def validate_token(token):
    # Validate the token

    if not token:
        return [False, {}]
    is_exist = frappe.db.exists({
        'doctype': 'Chat Guest',
        'token': token,
    })

    if not is_exist:
        return [False, {}]

    guest_user = frappe.get_doc('Chat Guest', str(is_exist[0][0]))

    if guest_user.ip_address != frappe.local.request_ip:
        return [False, {}]

    existing_room = frappe.db.get_list(
        'Chat Room', filters={'guest': guest_user.email})
    room = existing_room[0]['name']

    guest_details = {
        'email': guest_user.email,
        'room': room,
    }
    return [True, guest_details]


def get_admin_name(user_key):
    full_name = frappe.db.get_value('User', user_key, 'full_name')
    return full_name


def update_room(room, last_message=None, is_read=0):
    doc_room = frappe.get_doc('Chat Room', room)
    doc_room.is_read = is_read

    if last_message:
        doc_room.last_message = last_message

    doc_room.save()
