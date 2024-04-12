
# @api_view(["POST"])
# def shopping_update(request,id,shop_id):
#     try:

#         # Instantiate FileSystemStorage
#         fs = FileSystemStorage()
        
#         # Retrieve existing shopping data
#         shop_data = shoppingmodel.objects.get(Business_id=id, shop_id=shop_id)
#         shop_datas = shoppingmodel.objects.filter(Business_id=id, shop_id=shop_id).values()[0]

#         # Handle file uploads
#         if "aadhar" in request.FILES:
#             aadhar = request.FILES['aadhar']
#             aadhar_path = fs.save(f"api/shopping/{id}/aadhar/{aadhar.name}", aadhar)
#             aadhar_paths = fs.url(aadhar_path)
#         else:
#             aadhar_paths = shop_datas["aadhar"]

#         if "pan_file" in request.FILES:
#             pan_file = request.FILES["pan_file"]
#             pan_file_path = fs.save(f"api/shopping/{id}/pan_file/{pan_file.name}", pan_file)
#             pan_file_paths = fs.url(pan_file_path)
#         else:
#             pan_file_paths = shop_datas["pan_file"]

#         if "profile" in request.FILES:
#             profile = request.FILES["profile"]
#             profile_path = fs.save(f"api/shopping/{id}/profile/{profile.name}", profile)
#             profile_paths = fs.url(profile_path)
#         else:
#             profile_paths = shop_datas["profile"]

#         if "bank_passbook" in request.FILES:
#             bank_passbook = request.FILES["bank_passbook"]
#             bank_passbook_path = fs.save(f"api/shopping/{id}/bank_passbook/{bank_passbook.name}", bank_passbook)
#             bank_passbook_paths = fs.url(bank_passbook_path)
#         else:
#             bank_passbook_paths = shop_datas["bank_passbook"]

#         if "gst_file" in request.FILES:
#             gst_file = request.FILES["gst_file"]
#             gst_file_path = fs.save(f"api/shopping/{id}/gst_file/{gst_file.name}", gst_file)
#             gst_file_paths = fs.url(gst_file_path)
#         else:
#             gst_file_paths = shop_datas["gst_file"]
        
#         # Update other fields

#         shop_data = shoppingmodel.objects.get(Business_id=id, shop_id=shop_id)
#         shop_data.seller_name = request.data.get('seller_name', shop_data.seller_name)
#         shop_data.business_name = request.data.get('business_name', shop_data.business_name)
#         shop_data.pan_number = request.data.get('pan_number', shop_data.pan_number)
#         shop_data.gst = request.data.get('gst', shop_data.gst)
#         shop_data.contact = request.data.get('contact', shop_data.contact)
#         shop_data.alternate_contact = request.data.get('alternate_contact', shop_data.alternate_contact)
#         shop_data.door_number = request.data.get('door_number', shop_data.door_number)
#         shop_data.street_name = request.data.get('street_name', shop_data.street_name)
#         shop_data.area = request.data.get('area', shop_data.area)
#         shop_data.region = request.data.get('region', shop_data.region)
#         shop_data.pin_number = request.data.get('pin_number', shop_data.pin_number)
#         shop_data.aadhar_number = request.data.get('aadhar_number', shop_data.aadhar_number)
#         shop_data.pin_your_location = request.data.get('pin_your_location', shop_data.pin_your_location)
#         shop_data.name = request.data.get('name', shop_data.name)
#         shop_data.account_number = request.data.get('account_number', shop_data.account_number)
#         shop_data.ifsc_code = request.data.get('ifsc_code', shop_data.ifsc_code)
#         shop_data.upi_id = request.data.get('upi_id', shop_data.upi_id)
#         shop_data.gpay_number = request.data.get('gpay_number', shop_data.gpay_number)
#         # Update other fields similarly

#         # Save changes
#         shop_data.aadhar = aadhar_paths
#         shop_data.pan_file = pan_file_paths
#         shop_data.profile = profile_paths
#         shop_data.bank_passbook = bank_passbook_paths
#         shop_data.gst_file = gst_file_paths
#         shop_data.save()

#         return Response(id, status=status.HTTP_200_OK)
#     except:
#         return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)





# @api_view(["POST"])
# def delivery_person_update(request,id):
#     if request.method=="POST":
#         fs=FileSystemStorage
#         # print(request.data)
#         # print(request.FILES)
#         d_data = models.Delivery_model.objects.get(uid=id)
#         print(d_data)
#         datas = models.Delivery_model.objects.filter(uid=id).values()[0]
#         print(datas)
#   if "pan_file" in request.FILES:
# #             pan_file = request.FILES["pan_file"]
# #             pan_file_path = fs.save(f"api/shopping/{id}/pan_file/{pan_file.name}", pan_file)
# #             pan_file_paths = fs.url(pan_file_path)
# #         else:

#         if "profile_picture" in request.FILES:
#             profile_picture = request.FILES["profile_picture"]
           
#             profile_picture_path = fs.save(f"api/delivery/{id}/profile_picture/{profile_picture.name}",profile_picture)
#             profile_picturepaths = fs.url(profile_picture_path)
#         else:
#             profile_picturepaths = datas["profile_picture"]
#             print(profile_picturepaths) 
#         if "bank_passbok_pic" in request.FILES:
#             bank_passbok_pic=request.FILES["bank_passbok_pic"]
#             bank_passbok_pic = str(request.FILES["pan_file"]).replace(" ","_")
#             bank_passbok_pic_path = fs.save(f"api/delivery/{id}/bank_passbok_pic/{bank_passbok_pic.name}",bank_passbok_pic)
#             bank_passbok_pic_paths = fs.url(bank_passbok_pic_path)
#         else:
#             bank_passbok_pic_paths = datas["bank_passbok_pic"]
#             print(bank_passbok_pic_paths)
#         if "aadhar_pic" in request.FILES:
#             aadhar_pic =request.FILES["aadhar_pic"]
#             aadhar_pic = str(request.FILES["aadhar_pic"]).replace(" ","_")
#             aadhar_pic_path = fs.save(f"api/delivery/{id}/aadhar_pic/{aadhar_pic.name}",aadhar_pic)
#             aadhar_pic_paths = fs.url(aadhar_pic_path)
#         else:
#             aadhar_pic_paths = datas["aadhar_pic"]
#             print(aadhar_pic_paths)
#         if "pan_pic" in request.FILES:
#             pan_pic= request.FILES["pan_pic"]
#             pan_pic = str(request.FILES["pan_pic"]).replace(" ","_")
#             pan_pic_path = fs.save(f"api/delivery/{id}/pan_pic/{pan_pic.name}",pan_pic)
#             pan_pic_paths =fs.url(pan_pic_path)
#         else:
#             pan_pic_paths = datas["pan_pic"]
#             print(pan_pic_paths)
#         if "drlicence_pic" in request.FILES:
#             drlicence_pic = request.FILES["drlicence_pic"]
#             drlicence_pic = str(request.FILES["drlicence_pic"]).replace(" ","_")
#             drlicence_pic_path = fs.save(f"api/delivery/{id}/drlicence_pic/{drlicence_pic.name}",drlicence_pic)
#             drlicence_pic_paths = fs.url(drlicence_pic_path)
#         else:
#             drlicence_pic_paths = datas["drlicence_pic"]
#             print(drlicence_pic_paths)
#         print(request.data)
        
#         d_data.name = request.data.get('name', d_data.name)
#         d_data.phone_number = request.data.get('phone_number', d_data.phone_number)
#         d_data.wp_number = request.data.get('wp_number', d_data.wp_number)
#         d_data.email = request.data.get('email', d_data.email)
#         d_data.aadhar_number = request.data.get('aadhar_number', d_data.aadhar_number)
#         d_data.driving_licensenum = request.data.get('driving_licensenum', d_data.driving_licensenum)
#         d_data.pan_number = request.data.get('pan_number', d_data.pan_number)
#         d_data.bank_name = request.data.get('bank_name', d_data.bank_name)
#         d_data.acc_number = request.data.get('acc_number', d_data.acc_number)
#         d_data.name_asper_passbook = request.data.get('name_asper_passbook', d_data.name_asper_passbook)
#         d_data.ifsc_code = request.data.get('ifsc_code', d_data.ifsc_code)
#         d_data.delivery_type = request.data.get('delivery_type', d_data.delivery_type)

        
#         d_data.profile_picture=profile_picturepaths,
#         d_data.bank_passbok_pic=bank_passbok_pic_paths,
#         d_data.aadhar_pic=aadhar_pic_paths,
#         d_data.pan_pic=pan_pic_paths,
#         d_data.drlicence_pic=drlicence_pic_paths,
#         d_data.save()
#         return Response(id, status=status.HTTP_200_OK)
        
#     else:
#         return Response({"serializer issue"}, status=status.HTTP_403_FORBIDDEN)