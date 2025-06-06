from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.core.paginator import Paginator
from voting.models import VotingCode
from candidates.models import Position, Candidate
from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from django.contrib import messages




# ✅ New Homepage (Vote Now Page)
def vote_now(request):
    error = None

    if request.method == "POST":
        if "code" in request.POST:  # Step 1: code validation
            code = request.POST.get("code", "").strip().upper()
            try:
                voting_code = VotingCode.objects.get(code=code)
                if voting_code.is_used:
                    error = "This code has already been used."
                else:
                    # Store code in session and redirect to vote page
                    request.session['voting_code'] = code
                    return redirect('cast_vote')
            except VotingCode.DoesNotExist:
                error = "Invalid code. Please try again."

    return render(request, 'home/votenow.html', {'error': error})

# ✅  View handling the vote logic
def cast_vote(request):
    code = request.session.get('voting_code', None)

    # 🛠️ Print current time and deadline for debugging
    print("⏱️ Current time:", timezone.now())
    print("🚫 Voting deadline:", settings.VOTING_END_TIME)

    # 🛑 Voting deadline check
    if timezone.now() > settings.VOTING_END_TIME:
        print("❌ Voting blocked — deadline has passed.")
        messages.error(request, "🕒 Voting has ended.")
        return redirect('homepage')
    else:
        print("✅ Voting allowed — still within deadline.")

    if not code:
        return redirect('homepage')  # Redirect if no valid voting session

    try:
        voting_code = VotingCode.objects.get(code=code)
        if voting_code.is_used:
            return redirect('homepage')  # Already used

        positions = Position.objects.prefetch_related('candidates').all()

        if request.method == "POST":
            for position in positions:
                candidate_id = request.POST.get(f"vote_{position.id}")
                if candidate_id:
                    try:
                        candidate = Candidate.objects.get(id=candidate_id, position=position)
                        candidate.votes += 1
                        candidate.save()
                    except Candidate.DoesNotExist:
                        continue  # Ignore invalid submissions

            # Mark the code as used
            voting_code.is_used = True
            voting_code.used_at = timezone.now()
            voting_code.save()

            # Clear session
            del request.session['voting_code']

            return render(request, "home/vote_success.html")

        return render(request, 'home/voting_page.html', {'positions': positions})

    except VotingCode.DoesNotExist:
        return redirect('homepage')
    except VotingCode.DoesNotExist:
        return redirect('homepage')


def view_results(request):
    positions = Position.objects.prefetch_related('candidates').all()

    for pos in positions:
        total = sum(c.votes for c in pos.candidates.all())
        pos.total_votes = total  # ✅ Attach total_votes directly to position

    return render(request, 'home/results.html', {'positions': positions})


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
    message = None
    positions = Position.objects.all()

    if request.method == "POST":
        surname = request.POST.get("surname")
        first_name = request.POST.get("first_name")
        student_class = request.POST.get("student_class")
        position_id = request.POST.get("position_id")

        if surname and first_name and student_class and position_id:
            position = Position.objects.get(id=position_id)
            Candidate.objects.create(
                surname=surname,
                first_name=first_name,
                student_class=student_class,
                position=position
            )
            message = f"{surname} {first_name} has been registered successfully!"

    return render(request, "home/register.html", {"positions": positions, "message": message})


# ✅ Delete All Codes (with confirmation)
@csrf_exempt
def delete_all_codes(request):
    if request.method == "POST":
        VotingCode.objects.all().delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'failed'}, status=400)
