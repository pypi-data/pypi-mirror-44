import pyfcm
from pyfcm import FCMNotification


#https://github.com/olucurious/PyFCM
def send_notification(registration_ids, message_body):

    push_service = FCMNotification(api_key="AAAAQEUZt1M:APA91bHctxd-8I9Mdc2bdIfo5OYm9leUfPOnVFzVg2xQ7xFwTPbsx5HwmzGx6TiHZzWBKaii8CRJ6NKhimnSR8X3Z0g6PEpsutpQekBm2-XbMKSDKcfHz7-3PhjFXHz7GM4e0CrbMAjc")
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=message_body)
    return result