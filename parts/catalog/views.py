# Catalog views.py

from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .models import *
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils import timezone

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


def valid_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif']
    valid = False
    if ext.lower() in valid_extensions:
        valid = True
    return valid
        

# @login_required(login_url='login-page')
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

# @login_required(login_url='login-page')
def item_page(request, model_number):
    part = Part.objects.get(model=model_number)
    part_type = part_types[part.part_type]
    laptops = part.laptop_model.all()
    return render(request, "base/item-page.html", {"model_number": model_number, "laptops": laptops, "model_name": part_type, "part": part})

# @login_required(login_url='login-page')
def home(request):

    recent_parts = list(Part.objects.all()[0:4])
    recent_laptops = list(Laptop.objects.all()[0:4])
    recent_parts = zip([recent_parts], ["part"])
    recent_laptops = zip([recent_laptops], ["laptop"])
    return render(request, 'base/home.html', {"part_results": recent_parts, "laptop_results": recent_laptops})

# @login_required(login_url='login-page')
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
                size = laptop_image.size
                print(size)
                if size > settings.MAX_UPLOAD_SIZE:
                    messages.info(request, f"Laptop image too large. Image not saved.")
                    raise SaveError
                if not valid_file_extension(laptop_image):
                    messages.info(request, f"Invalid file extension. Image not saved.")
                    raise SaveError
                try:
                    laptop.image = laptop_image
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
    try:
        laptop = Laptop.objects.get(laptop_model=laptop_model)
    except Exception as e:
        messages.info(request, f"Unable to find laptop model {laptop_model}. Try again or notify administrator.")
        return redirect('home-page')
    
    
    if request.method == "POST":
        
        model_numbers = []
        model_number_images = []


        laptop_image = request.FILES.get('laptop-image')
        if laptop_image:
            size = laptop_image.size
            if size > settings.MAX_UPLOAD_SIZE:
                messages.info(request, f"Laptop image too large. Image not saved.")
                raise SaveError
            if not valid_file_extension(laptop_image):
                messages.info(request, f"Invalid file extension. Image not saved.")
                raise SaveError
            try:
                laptop.image = laptop_image
                laptop.save()
            except Exception as e:
                print(e)
                messages.info(request, f"Unable to save laptop image. Try again or notify administrator.")
                raise SaveError
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
        
        # Update part data
        try:
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
                        if not is_member(user, "admin"):
                            if model_image and "/default.png" in part.image.url.lower():
                                if valid_file_extension(model_image.name):
                                    if model_image.size > settings.MAX_UPLOAD_SIZE:
                                        messages.debug(request, f"{model_number} image too large. Choose a new image or notify administrator.")
                                        raise SaveError
                                    part.image = model_image
                                    part.save()
                                else: messages.error(request, f"{model_number} image is not a valid file type. Choose a new image or notify administrator.")
                                raise SaveError
                        else:
                            if model_image and valid_file_extension(model_image.name):
                                part.image = model_image
                                part.save()
                            elif not valid_file_extension(model_image.name):
                                messages.error(request, f"{model_number} image is not a valid file type. Choose a new image.")
                                raise SaveError
                            
                    except Exception as e:
                        print(e)
                        messages.error(request, f"Unable to add model number: {model_number} with part type: {part_type}. Check info or notify administrator.")
                        raise SaveError
                    try:
                        part = Part.objects.filter(model=model_number).filter(laptop_model=laptop.id)
                        if not part:
                            part.laptop_model.add(laptop.id)
                    except Exception as e:
                        print(e)
                        messages.error(request, f"Unable to link model number: {model_number} to laptop: {laptop_model}. Check info or notify administrator.")
                        raise SaveError
        except SaveError:
            return render(request, 'base/edit-laptop.html', {"laptop": laptop})    
        
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

    return render(request, "base/edit-laptop-data.html", {'laptop_model': laptop_model, 'laptop_image_url': laptop.image.url, 'form_data': form_data})

@login_required(login_url='login-page')
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

@login_required(login_url='login-page')
def part_upvote(request):
    user = request.user
    if user.is_authenticated:
        if request.method == "POST":
            part_id = request.POST.get("partid")
            part = Part.objects.get(id=part_id)
            user = request.user
            if user.is_authenticated:
                result = part.upvote(user)
                if "removed" in result.lower():
                    return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "removed"})
                return JsonResponse({"response": result, "bool": True, "score": part.score, "vote_type": "upvote"})
    else:
        messages.info(request, "You must be logged in to vote.")
        return redirect('login-page', next=request.path)

@login_required(login_url='login-page')
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

@login_required(login_url='login-page')
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

@login_required(login_url='login-page')
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

@login_required(login_url='login-page')
def part_model_change(request, part_model):
    
    part_model_change_form = ModelChangeForm()
    part_model_change_form.fields['current_model'].initial = part_model

    if request.method == "POST":
        
        suggested_part_model = request.POST.get("suggested_model")

        if suggested_part_model == part_model:
            messages.info(request, "You cannot change to the same model.")
            return render(request, "base/new-model-suggest.html", {'model_change_form': part_model_change_form, "model": part_model})

        try:
            part = Part.objects.get(model=part_model)
        except:
            messages.error(request, "Part model not found.")
            return render(request, "base/new-model-suggest.html", {'model_change_form': part_model_change_form, "model": part_model})
        
        try:
            suggested_part = Part.objects.get(model=suggested_part_model)
            messages.info(request, "Part model already exists. Redirected to page.")
            return redirect('item-page', model_number=suggested_part_model)
        except:
            pass

        try:
            part_model_change = PartModelChange.objects.filter(part=part).filter(old_model=part_model).filter(new_model=suggested_part_model)
            if part_model_change.exists():
                if not part_model_change[0].approved:
                    if not part_model_change[0].rejected_by and not part_model_change[0].approved_by:
                        messages.error(request, "This change has already been suggested for this model. Please wait for mods to review.")
                        return redirect('item-page', model_number=part_model)
                    messages.error(request, "This part model change has already been suggested and was denied after review by mods. Please contact an administrator if you believe this to be an error.")
                    return redirect('item-page', model_number=part_model)
                messages.success(request, "This part model change has already been suggested and was approved after review by mods. Please contact an administrator if you believe this to be an error.")
                return redirect('item-page', model_number=part_model)
        except:
            pass


        PartModelChange.objects.create(part=part, old_model=part_model, new_model=suggested_part_model, created_by=request.user)
        messages.success(request, "Thank you for the model change suggestion. Mods will review and approve this change if appropriate.")
        return redirect('item-page', model_number=part_model)
    
    return render(request, "base/new-model-suggest.html", {'model_change_form': part_model_change_form, 'model': part_model})

@login_required(login_url='login-page')
def laptop_model_change(request, laptop_model):
        
    laptop_model_change_form = ModelChangeForm()
    laptop_model_change_form.fields['current_model'].initial = laptop_model

    if request.method == "POST":
        
        suggested_laptop_model = request.POST.get("suggested_model")

        if suggested_laptop_model == laptop_model:
            messages.info(request, "You cannot change to the same model.")
            return render(request, "base/new-model-suggest.html", {'model_change_form': laptop_model_change_form, "model": laptop_model})

        try:
            laptop = Laptop.objects.get(laptop_model=laptop_model)
        except:
            messages.error(request, "Laptop model not found.")
            return render(request, "base/new-model-suggest.html", {'model_change_form': laptop_model_change_form, "model": laptop_model})
        
        try:
            suggested_laptop = Laptop.objects.get(laptop_model=suggested_laptop_model)
            messages.info(request, "Laptop model already exists. Redirected to page.")
            return redirect('laptop-page', laptop_model=suggested_laptop_model)
        except:
            pass

        try:
            laptop_model_change = LaptopModelChange.objects.filter(laptop=laptop).filter(old_model=laptop_model).filter(new_model=suggested_laptop_model)
            if laptop_model_change.exists():
                if not laptop_model_change[0].approved:
                    if not laptop_model_change[0].rejected_by and not laptop_model_change[0].approved_by:
                        messages.error(request, "This change has already been suggested for this model. Please wait for mods to review.")
                        return redirect('laptop-page', laptop_model=laptop_model)
                    messages.error(request, "This laptop model change has already been suggested and was denied after review by mods. Please contact an administrator if you believe this to be an error.")
                    return redirect('laptop-page', laptop_model=laptop_model)
                messages.success(request, "This laptop model change has already been suggested and was approved after review by mods. Please contact an administrator if you believe this to be an error.")
                return redirect('laptop-page', laptop_model=laptop_model)
        except:
            pass

        LaptopModelChange.objects.create(laptop=laptop, old_model=laptop_model, new_model=suggested_laptop_model, created_by=request.user)
        messages.success(request, "Thank you for the model change suggestion. Mods will review and approve this change if appropriate.")
        return redirect('laptop-page', laptop_model=laptop_model)

    return render(request, "base/new-model-suggest.html", {'model_change_form': laptop_model_change_form, 'model': laptop_model})

@login_required(login_url='login-page')

def requested_part_changes(request):
    
    if not is_member(request.user, "mod"):
        return redirect('home')
    
    part_model_changes = PartModelChange.objects.filter(rejected_by=None).filter(approved_by=None)
    part_model_changes = list(part_model_changes)
    part_types_change = []
    for part_change in part_model_changes:
        part_type = Part.objects.get(model=part_change.old_model).part_type
        part_types_change.append(part_types[part_type])
    parts_data = zip(part_model_changes, part_types_change)
    
    return render(request, "base/requested-part-changes.html", {'parts_data': parts_data})

@login_required(login_url='login-page')
def requested_part_change_review(request, part_model_change_id):

    if not is_member(request.user, "mod"):
        return redirect('home')

    part_model_change = PartModelChange.objects.get(id=part_model_change_id)
    part = Part.objects.get(model=part_model_change.old_model)
    part_type = part_types[part.part_type]

    if request.method == "POST":

        if request.POST.get("option") not in ["approved", "rejected"]:
            messages.error(request, "Please select either approve or reject.")
            return render(request, "base/requested-part-change-review.html", {'part': part_model_change, 'part_type': part_type})
        
        if request.POST.get("option") == "approved":
            try:
                part_model_change.approved = True
                part_model_change.approved_by = request.user
                part_model_change.approved_date = timezone.now()
                part_model_change.save()
            except Exception as e:
                messages.error(request, f"Error approving part model change: {e}")
                return render(request, "base/requested-part-change-review.html", {'part': part_model_change, 'part_type': part_type})
            try:
                part = Part.objects.get(model=part_model_change.old_model)
                part.model = part_model_change.new_model
                part.save()
            except Exception as e:
                messages.error(request, f"Error changing part model in current database: {e}")
                return render(request, "base/requested-part-change-review.html", {'part': part_model_change, 'part_type': part_type})
            messages.success(request, f"{part_type} model change approved and succesfully changed in current database.")
            return redirect('requested-part-changes')
        elif request.POST.get("option") == "rejected":
            part_model_change.rejected = True
            part_model_change.rejected_by = request.user
            part_model_change.rejected_date = timezone.now()
            part_model_change.rejected_reason = request.POST.get("reason")
            part_model_change.save()
            messages.success(request, f"{part_type} model change rejected.")
            return redirect('requested-part-changes')

    return render(request, "base/requested-part-change-review.html", {'part': part_model_change, 'part_type': part_type})

@login_required(login_url='login-page')
def requested_laptop_changes(request):

    if not is_member(request.user, "mod"):
        return redirect('home')

    laptop_model_changes = LaptopModelChange.objects.filter(rejected_by=None).filter(approved_by=None)
    laptop_model_changes = list(laptop_model_changes)
    
    return render(request, "base/requested-laptop-changes.html", {'laptops': laptop_model_changes})

@login_required(login_url='login-page')
def requested_laptop_change_review(request, laptop_model_change_id):

    if not is_member(request.user, "mod"):
        return redirect('home')

    laptop_model_change = LaptopModelChange.objects.get(id=laptop_model_change_id)

    if request.method == "POST":

        if request.POST.get("option") not in ["approved", "rejected"]:
            messages.error(request, "Please select either approve or reject.")
            return render(request, "base/requested-laptop-change-review.html", {'laptop': laptop_model_change})
        
        if request.POST.get("option") == "approved":
            try:
                laptop_model_change.approved = True
                laptop_model_change.approved_by = request.user
                laptop_model_change.approved_date = timezone.now()
                laptop_model_change.save()
            except Exception as e:
                messages.error(request, f"Error approving laptop model change: {e}")
                return render(request, "base/requested-laptop-change-review.html", {'laptop': laptop_model_change})
            try:
                laptop = Laptop.objects.get(laptop_model=laptop_model_change.old_model)
                laptop.laptop_model = laptop_model_change.new_model
                laptop.save()
            except Exception as e:
                messages.error(request, f"Error changing laptop model in current database: {e}")
                return render(request, "base/requested-laptop-change-review.html", {'laptop': laptop_model_change})
            messages.success(request, f"Laptop model change approved and succesfully changed in current database.")
            return redirect('requested-laptop-changes')
        elif request.POST.get("option") == "rejected":
            laptop_model_change.rejected = True
            laptop_model_change.rejected_by = request.user
            laptop_model_change.rejected_date = timezone.now()
            laptop_model_change.rejected_reason = request.POST.get("reason")
            laptop_model_change.save()
            messages.success(request, f"Laptop model change rejected.")
            return redirect('requested-laptop-changes')
    
    return render(request, "base/requested-laptop-change-review.html", {'laptop': laptop_model_change})


@login_required(login_url='login-page')
def confirm_delete_laptop(request, laptop_id):

    if not is_member(request.user, "mod"):
        return redirect('home')

    laptop = Laptop.objects.get(id=laptop_id)
    model_number = laptop.laptop_model
    type_to_delete = 'Laptop'

    if request.method == "POST":
        if request.POST.get("option") == "delete":
            try:
                laptop.delete()
                messages.success(request, f"Laptop deleted.")
            except Exception as e:
                messages.error(request, f"Error deleting laptop: {e}")
            return redirect('home')
        elif request.POST.get("option") == "cancel":
            messages.info(request, f"Deletion cancelled.")
            return redirect('home')

    return render(request, "base/confirm-delete.html", {'model_number': model_number, 'type_to_delete': type_to_delete})

@login_required(login_url='login-page')
def confirm_delete_part(request, part_id):
    
    if not is_member(request.user, "mod"):
        return redirect('home')

    part = Part.objects.get(id=part_id)
    model_number = part.model
    type_to_delete = part_types[part.part_type]

    if request.method == "POST":
        if request.POST.get("option") == "delete":
            try:
                part.delete()
                messages.success(request, f"Part deleted.")
            except Exception as e:
                messages.error(request, f"Error deleting part: {e}")
            return redirect('home')
        elif request.POST.get("option") == "cancel":
            messages.info(request, f"Deletion cancelled.")
            return redirect('home')

    return render(request, "base/confirm-delete.html", {'model_number': model_number, 'type_to_delete': type_to_delete})

@login_required(login_url='login-page')
def verify_part(request, part_id):

    if not is_member(request.user, "mod"):
        return redirect('home')

    part = Part.objects.get(id=part_id)
    model_number = part.model
    part_type = part_types[part.part_type]
    is_verified = part.verified
    print(part.verified)

    if request.method == "POST":
        print(request.POST)
        if request.POST.get("option") == "verify":
            try:
                part.verified = True
                part.verified_by = request.user
                part.verified_date = timezone.now()
                part.save()
            except Exception as e:
                messages.error(request, f"Error verifying part: {e}")
                return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})
            messages.success(request, f"{part_type} - {model_number} verified.")
            return redirect('item-page', model_number=model_number)
        elif request.POST.get("option") == "unverify":
            try:
                part.verified = False
                part.verified_by = None
                part.verified_date = None
                part.save()
            except Exception as e:
                messages.error(request, f"Error unverifying part: {e}")
                return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})
            messages.success(request, f"{part_type} - {model_number} unverified.")
            return redirect('item-page', model_number=model_number)
        elif request.POST.get("option") == "cancel":
            messages.info(request, f"Verification cancelled.")
            return redirect('item-page', model_number=model_number)

    return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})

@login_required(login_url='login-page')
def verify_laptop(request, laptop_id):

    if not is_member(request.user, "mod"):
        return redirect('home')

    laptop = Laptop.objects.get(id=laptop_id)
    model_number = laptop.laptop_model
    part_type = 'Laptop'
    is_verified = laptop.verified

    if request.method == "POST":
        if request.POST.get("option") == "verify":
            try:
                laptop.verified = True
                laptop.verified_by = request.user
                laptop.verified_date = timezone.now()
                laptop.save()
            except Exception as e:
                messages.error(request, f"Error verifying laptop: {e}")
                return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})
            messages.success(request, f"Laptop - {model_number} verified.")
            return redirect('laptop-page', laptop_model=model_number)
        elif request.POST.get("option") == "unverify":
            try:
                laptop.verified = False
                laptop.verified_by = None
                laptop.verified_date = None
                laptop.save()
            except Exception as e:
                messages.error(request, f"Error unverifying laptop: {e}")
                return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})
            messages.success(request, f"Laptop - {model_number} unverified.")
            return redirect('laptop-page', laptop_model=model_number)
        elif request.POST.get("option") == "cancel":
            messages.info(request, f"Verification cancelled.")
            return redirect('laptop-page', laptop_model=model_number)

    return render(request, "base/confirm-verify.html", {'model_number': model_number, 'type_to_verify': part_type, 'is_verified': is_verified})
    