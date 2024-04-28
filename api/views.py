
# @api_view(['POST'])
# def delivery_notification(request):
#     if request.method == "POST":
#         print(request.data)
#         sender_id = request.data.get('sender_id')
#         recever_id = request.data.get('recever_id')
        
#         # Check if a notification with the same sender_id and receiver_id already exists
#         existing_notification = models.Notification.objects.filter(sender_id=sender_id, recever_id=recever_id).first()
        
#         if existing_notification:
#             # Append the new notification message to the existing list of messages
#             existing_notification.notify_message.append(request.data.get('notify_message'))
#             existing_notification.save()
#             print("Notification message appended to existing list")
#             return Response('success', status=status.HTTP_200_OK)
#         else:
#             # Create a new notification entry
#             data = {
#                 'notify_id': delivery_extension.id_generate(),
#                 'sender_id': sender_id,
#                 'notify_message': [request.data.get('notify_message')],
#                 'recever_id': recever_id,
#             }
#             basic_details_serializer = delivery_serializers.notificationSerializer(data=data)
#             if basic_details_serializer.is_valid():
#                 basic_details_serializer.save()
#                 print("New notification message saved")
#                 return Response('success', status=status.HTTP_200_OK)
#             else:
#                 print("Invalid data")
#                 return Response({"serializer problem"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        












        
@api_view(["POST"])
def delivery_verify_otp(request,id):
    print(request.POST)
    otp = request.POST.get('otp')
    uid = delivery_extension.id_generate()
    print(uid)
    if not otp or not uid:
        return Response({"error": "OTP and UID are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Retrieve the OTP instance from the database
        otp_instance = models.Delivery_model.objects.get(otp=otp, uid=uid)
        
        # Retrieve the phone number associated with the OTP instance
        phone_number = otp_instance.phone_number
        
        # Here, you can add logic to match the phone number with the one already saved in the database
        # Assuming phone_number is already saved in the database and sent in the request
        # If the phone numbers don't match, return an error response
        if phone_number != request.POST.get('phone_number'):
            return Response({"error": "OTP does not match the provided phone number"}, status=status.HTTP_400_BAD_REQUEST)

        # OTP and phone number match, you can proceed with further actions
        # For example, you can mark this OTP instance as verified
        
        # otp_instance.verified = True
        # otp_instance.save()

        return Response(uid, status=status.HTTP_200_OK)
    except models.Delivery_model.DoesNotExist:
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)




        