from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from voting.models import VotingCode

# ✅ New Homepage (Vote Now Page)
def vote_now(request):
    return render(request, 'home/votenow.html')

# ✅ Renamed Generate Codes View
@csrf_exempt
def generate_codes(request):
    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))
        VotingCode.create_codes(qty)
        message = f"{qty} code{'s' if qty != 1 else ''} generated successfully"
        return JsonResponse({"message": message})
    return render(request, 'home/generatecodes.html')

# ✅ Print Page with Pagination
def print_page(request):
    codes_list = VotingCode.objects.all().order_by('-id')
    paginator = Paginator(codes_list, 125)  # 5 x 25 layout
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home/print.html', {'page_obj': page_obj})

# ✅ Register Participants Page
def register_participants(request):
    return render(request, 'home/register.html')

# ✅ Delete All Codes (with confirmation)
@csrf_exempt
def delete_all_codes(request):
    if request.method == "POST":
        VotingCode.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
