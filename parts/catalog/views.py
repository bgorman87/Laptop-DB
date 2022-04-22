# Catalog views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
import sys
from users.decorators import allowed_users

part_types = {
    'KEYB': 'Keyboard',
    'BOTC': 'Bottom Cover',
    'PALR': 'Palm Rest',
    'LCDC': 'LCD Cover',
    'LCD': 'LCD',
    'LCDB': 'LCD Bezel',
    'LCDT': 'LCD Touch Assembly',
    'TRA': 'Track pad',
    'SPE': 'Speakers',
    'MIC': 'Microphone',
    'CAM': 'Camera',
    'POW': 'Power Button',
    'HEAT': 'Heat sink',
    'CDD': 'CD Drive',
    'WIFI': 'Wi-Fi Adapter',
    'MOTH': 'Motherboard',
    'WIFA': 'Wi-Fi Antenna',
    'DICA': 'Display Cable',
    'HDDC': 'Hard Drive Caddy',
    'TPFC': 'Track pad Flex Cable',
    'PBFC': 'Power Button Flex Cable',
    'SB01': 'Sub Board 1',
    'SB02': 'Sub Board 2',
    'SB03': 'Sub Board 3',
    'SBFC': 'Sub Board Flex Cable',
    'CHAR': 'Charger',
    'BATT': 'Battery',
    'CHRP': 'Charging Port',
    'CPUF': 'CPU Fan',
    'LFTH': 'Left Hinge',
    'RGTH': 'Right Hinge',
    'SAT': 'SATA',
    'SATC': 'SATA Cable',
    'POR': 'Ports',
    'GRAC': 'Graphics Card',
    'RAM': 'RAM'
    }

def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

class SaveError(Exception):
    pass


# def image_upload(image_file):
#     print(image_file, file=sys.stderr)
#     if settings.USE_S3:
#         upload = Upload(file=image_file)
#         print(upload, file=sys.stderr)
#         upload.save()
#         image_url = upload.file.url
#     else:
#         fs = FileSystemStorage()
#         filename = fs.save(image_file.name, image_file)
#         image_url = fs.url(filename)
#     return image_url
        

@login_required(login_url='login-page')
def laptop_page(request, laptop_model):
    
    keyboards = []
    bottom_covers = []
    palm_rests = []
    lcd_covers = []
    lcds = []
    lcd_bezels = []
    lcd_touch_assemblies = []
    track_pads = []
    speakers = []
    microphones = []
    cameras = []
    power_buttons = []
    heat_sinks = []
    cd_drives = []
    wifi_adapters = []
    motherboards = []
    wifi_antennas = []
    display_cables = []
    hard_drive_caddies = []
    track_pad_flex_cables = []
    power_button_flex_cables = []
    sub_boards_1 = []
    sub_boards_2 = []
    sub_boards_3 = []
    sub_board_flex_cables = []
    chargers = []
    batteries = []
    charging_ports = []
    cpu_fans = []
    left_hinges = []
    right_hinges = []
    satas = []
    sata_cables = []
    ports = []
    graphics_cards = []
    rams = []

    parts_lists = [keyboards , bottom_covers, palm_rests, lcd_covers, lcds, lcd_bezels, lcd_touch_assemblies, track_pads, speakers, microphones, cameras, power_buttons, heat_sinks, cd_drives, wifi_adapters, motherboards, wifi_antennas, display_cables, hard_drive_caddies, track_pad_flex_cables, power_button_flex_cables, sub_boards_1, sub_boards_2, sub_boards_3, sub_board_flex_cables, chargers, batteries, charging_ports, cpu_fans, left_hinges, right_hinges, satas, sata_cables, ports, graphics_cards, rams]

    laptop = Laptop.objects.get(laptop_model=laptop_model)
    active_parts = []

    for parts_list, part_type in zip(parts_lists, part_types.keys()):

        parts = Part.objects.filter(laptop_model=laptop.id).filter(part_type=part_type)

        if parts:
            parts_list.append(parts)
            active_parts.append(part_type)
    non_active_parts = [part_types[part_type] for part_type in part_types.keys() if part_type not in active_parts]
    parts_lists = [parts_list for parts_list in parts_lists if parts_list]
    parts_data = zip(parts_lists, [part_types[active_part_type] for active_part_type in active_parts])

    return render(request, "base/laptop-page.html", {"laptop": laptop, "parts": parts_data, "non_active": non_active_parts})

@login_required(login_url='login-page')
def item_page(request, model_number):
    part = Part.objects.get(model=model_number)
    part_type = part_types[part.part_type]
    laptops = part.laptop_model.all()
    return render(request, "base/item-page.html", {"model_number": model_number, "laptops": laptops, "model_name": part_type, "part": part})

@login_required(login_url='login-page')
def home(request):

    recent_parts = list(Part.objects.all()[0:4])
    recent_laptops = list(Laptop.objects.all()[0:4])
    recent_parts = zip([recent_parts], ["part"])
    recent_laptops = zip([recent_laptops], ["laptop"])
    return render(request, 'base/home.html', {"part_results": recent_parts, "laptop_results": recent_laptops})

@login_required(login_url='login-page')
def search_results(request):
    p = request.GET.get('p') if request.GET.get('p') != None else ''
    if p:
        part_type = list(Part.objects.filter(part_type__icontains=p))
        model_number = list(Part.objects.filter(model__icontains=p))
        laptop = list(Laptop.objects.filter(laptop_model__icontains=p))

        part_results = zip([part_type + model_number], ["part"])
        laptop_results = zip([laptop], ["laptop"])

        return render(request, 'base/search-results.html', {"part_results": part_results, "laptop_results": laptop_results, "search_query": p})
    return render(request, 'base/search-results.html', {"results": ''})

@login_required(login_url='login-page')
def add_laptop(request):
    user = request.user

    if request.method == "POST":
        
        # Initialize form to fill in incase of error
        laptop_form = LaptopForm(request.POST, request.FILES)

        # Check if model number was given and if not then return message with form data
        laptop_model = request.POST.get('laptop_model').replace(" ","")
        
        if not laptop_model:
            messages.error(request, f"Please enter a valid model number.")
            return render(request, 'base/add-laptop.html', {"form": laptop_form})
        
        # Check if model number already exists
        # If it does then dont even check manufacturer/series just go to page
        try:
            laptop = Laptop.objects.get(laptop_model=laptop_model)
            messages.info(request, f"{laptop_model} found. Update data if available.")
            # redirect to laptop page
            return redirect(f"/laptop/{laptop_model}")
        except Exception as e:
            pass
        
        # Check if manufacturer and series were given and if not then return message with form data
        manufacturer = request.POST.get('manufacturer')
        series = request.POST.get('series')
        if not manufacturer or not series:
            messages.error(request, f"Please enter a valid manufacturer and series.")
            return render(request, 'base/add-laptop.html', {"form": laptop_form})
        
        try:
            Laptop.objects.create(
                laptop_model=laptop_model,
                created_by=user,
                image='default.png',
            )
        except Exception as e:
            messages.info(request, f"Unable to add laptop model {laptop_model}. Try again or notify administrator.")
            return render(request, 'base/add-laptop.html', {"form": laptop_form})


        try:
            laptop = Laptop.objects.get(laptop_model=laptop_model)
            try:
                laptop.manufacturer = request.POST.get('manufacturer')
                laptop.save()
            except Exception as e:
                print(e)
                messages.info(request, f"Unable to save laptop manufacturer. Try again or notify administrator.")
                raise SaveError

            try:
                laptop.series = request.POST.get('series')
                laptop.save()
            except Exception as e:
                print(e)
                messages.info(request, f"Unable to save laptop series. Try again or notify administrator.")
                raise SaveError

            try:
                serial_number = request.POST.get('serial_number')
                try:
                    serial_number_object = Serial_Number.objects.get(serial_number=serial_number)
                except:
                    try:
                        Serial_Number.objects.create(
                            serial_number=serial_number
                        )
                    except Exception as e:
                        print(e)
                        messages.info(request, f"Unable to create serial number to add to laptop data. Try again or notify administrator.")
                        raise SaveError
                try:
                    serial_number_object = Serial_Number.objects.get(serial_number=serial_number)
                    laptop.serial_number.add(serial_number_object.id)
                except:
                    messages.info(request, f"Unable to connect serial number to laptop. Try again or notify administrator.")
                    raise SaveError
            except:
                messages.info(request, f"Unexpected error with serial number. Try again or notify administrator.")
                raise SaveError
            
            try:
                laptop.country_id = request.POST.get('country_id')
                laptop.save()
            except Exception as e:
                print(e)
                messages.info(request, f"Unable to save laptop country. Try again or notify administrator.")
                raise SaveError
            
            laptop_image = request.FILES.get('laptop-image')
            if laptop_image:
                try:
                    laptop.image = laptop_image
                    print(laptop.image.url, file=sys.stderr)
                    laptop.save()
                except Exception as e:
                    print(e)
                    messages.info(request, f"Unable to save laptop image. Try again or notify administrator.")
                    raise SaveError
        except SaveError:
            return render(request, 'base/add-laptop.html', {"form": laptop_form})            
            
        messages.success(request, "Thank you for adding to our database.")
        return redirect('edit-laptop', laptop_model=laptop_model)

    laptop_form = LaptopForm()
    return render(request, "base/add-laptop.html", {'form': laptop_form})
    
@login_required(login_url='login-page')
def edit_laptop(request, laptop_model):
    
    user = request.user
    laptop = Laptop.objects.get(laptop_model=laptop_model)
  
    if request.method == "POST":
        
        model_numbers = []
        model_number_images = []


        for part_type in part_types.keys():

            try:
                model_number = request.POST.get(part_type)
            except:
                model_number = ''
            try:
                model_number_image = request.FILES.get(f"{part_type}-image")
            except:
                model_number_image = ''

            model_number_images.append(model_number_image)
            model_numbers.append(model_number)

        error = False
        
        # Update part data
        for part_type, model_number, model_image in zip(part_types, model_numbers, model_number_images):
            if model_number:
                try:
                    try:
                        part = Part.objects.get(model=model_number)
                    except:
                        part = Part.objects.create(
                            model=model_number,
                            part_type=part_type,
                            created_by=user,
                            image='default.png',
                        )
                        part.laptop_model.add(laptop.id)
                    # Check if new image is given and if existing image is default, if so then overwrite
                    if model_image and "/default.png" in part.image.url.lower():
                        part.image = model_image
                        part.save()
                        
                except Exception as e:
                    print(e)
                    messages.error(request, f"Unable to add model number: {model_number} with part type: {part_type}. Check info or notify administrator.")

                try:
                    part = Part.objects.filter(model=model_number).filter(laptop_model=laptop.id)
                    if not part:
                        part.laptop_model.add(laptop.id)
                except Exception as e:
                    print(e)
                    messages.error(request, f"Unable to link model number: {model_number} to laptop: {laptop_model}. Check info or notify administrator.")
                    error = True
            
        if not error:
            messages.success(request, "Thank you for adding to our database.")
            return redirect(f"/laptop/{laptop_model}")

    forms = []

    # Check is user is a mod. If so show all form fields, if not show only blank fields
    part_types_list = list(part_types.keys())
    part_types_full_names_list = list(part_types.values())
    used_part_types_list = []
    used_part_types_full_names_list = []
    for i, part_type in enumerate(part_types_list):
        try:
            part = Part.objects.filter(laptop_model=laptop.id).filter(part_type=part_type)
            part = part[0]
            if part and (is_member(user, "mod") or is_member(user, "admin")):
                part_form = PartForm(instance=part)
                forms.append(part_form)
                used_part_types_list.append(part_type)
                used_part_types_full_names_list.append(part_types_full_names_list[i])
            elif not part:
                part_form = PartForm(instance=user)
                forms.append(part_form)
                used_part_types_list.append(part_type)
                used_part_types_full_names_list.append(part_types_full_names_list[i])
        except Exception as e:
            part_form = PartForm(instance=user)
            forms.append(part_form)
            used_part_types_list.append(part_type)
            used_part_types_full_names_list.append(part_types_full_names_list[i])
    
    form_data = zip(forms, used_part_types_full_names_list, used_part_types_list)

    return render(request, "base/edit-laptop-data.html", {'laptop_model': laptop_model, 'form_data': form_data})

# Basic users can only edit missing laptop parts
def user_add_laptop_data(request, laptop_model):

    user = request.user

    laptop = Laptop.objects.get(laptop_model=laptop_model)

    forms = []
    form_data = []
    for part_type in part_types.keys():
        try:
            part = Part.objects.filter(laptop_model=laptop.id).filter(part_type=part_type)
            part=part[0]
            part_form = PartForm(instance=part)
        except Exception as e:
            part_form = PartForm(instance=user)
        forms.append(part_form)    

    return render(request, "base/edit-laptop-data.html", {'laptop_model': laptop_model, 'form_data': form_data})

def part_upvote(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            part_id = request.POST.get("partid")
            part = Part.objects.get(id=part_id)
            user = request.user
            if user.is_authenticated:
                result = part.upvote(user)
                print(result)
                if "removed" in result.lower():
                    return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "removed"})
                return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "upvote"})
    else:
        messages.info(request, "You must be logged in to vote.")
        return redirect('login-page', next=request.path)

def part_downvote(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            part_id = request.POST.get("partid")
            part = Part.objects.get(id=part_id)
            user = request.user
            if user.is_authenticated:
                result = part.downvote(user)
                if "removed" in result.lower():
                    return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "removed"})
                return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "downvote"})
    else:
        messages.info(request, "You must be logged in to vote.")
        return redirect('login-page', next=request.path)

def laptop_upvote(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            laptop_id = request.POST.get("laptopid")
            laptop = Laptop.objects.get(id=laptop_id)
            user = request.user
            if user.is_authenticated:
                result = laptop.upvote(user)
                if "removed" in result.lower():
                    return JsonResponse({"response": result, "bool": True, "score": laptop.score, "vote_type": "removed"})
                return JsonResponse({"response": result, "bool": True, "score": laptop.score, "vote_type": "upvote"})

    else:
        messages.info(request, "You must be logged in to vote.")
        return redirect('login-page', next=request.path)

def laptop_downvote(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            laptop_id = request.POST.get("laptopid")
            laptop = Laptop.objects.get(id=laptop_id)
            user = request.user
            if user.is_authenticated:
                result = laptop.downvote(user)
                if "removed" in result.lower():
                    return JsonResponse({"response": result, "bool": True, "score": laptop.score, "vote_type": "removed"})
                return JsonResponse({"response": result, "bool": True, "score": laptop.score, "vote_type": "downvote"})
    else:
        messages.info(request, "You must be logged in to vote.")
        return redirect('login-page', next=request.path)

