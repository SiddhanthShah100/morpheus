from django.shortcuts import render, get_object_or_404, redirect
from .models import Form, Question, Response, Answer, Option
from django.db.models import Q
from collections import Counter
from .serializers import FormSerializer, ResponseSerializer
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
import json


def create_form(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                title = request.POST.get('title')
                description = request.POST.get('description')

                form = Form.objects.create(title=title, description=description)

                question_keys = [key for key in request.POST if key.startswith('questions[') and key.endswith('[text]')]

                for key in question_keys:
                    question_id = key.split('[')[1].split(']')[0]

                    question_text = request.POST.get(f'questions[{question_id}][text]')
                    question_type = request.POST.get(f'questions[{question_id}][type]')
                    options = [
                        request.POST.get(f'questions[{question_id}][options][{i}]')
                        for i in range(1, 4)
                        if request.POST.get(f'questions[{question_id}][options][{i}]')
                    ]
                    min_value = request.POST.get(f'questions[{question_id}][min_value]')
                    max_value = request.POST.get(f'questions[{question_id}][max_value]')

                    question = Question.objects.create(
                        form=form,
                        question_text=question_text,
                        question_type=question_type,
                        min_value=min_value if min_value else None,
                        max_value=max_value if max_value else None,
                        order=int(question_id),
                    )

                    for option_text in options:
                        Option.objects.create(question=question, option_text=option_text)

                return redirect('view_forms')
        except Exception as e:
            return render(request, 'create_form.html', {'error': str(e)})

    return render(request, 'create_form.html')



@login_required
def view_forms(request):
    forms = Form.objects.all()
    return render(request, 'view_form.html', {'forms': forms})


@login_required
def view_responses(request, form_id):
    form = get_object_or_404(Form, id=form_id)

    responses = form.responses.all()

    response_data = []
    for response in responses:
        answer_data = {}

        answers = Answer.objects.filter(response=response)

        for answer in answers:
            answer_data[answer.question.question_text] = answer.get_answer()

        response_data.append({
            'user': response.user,
            'answers': answer_data
        })

    return render(request, 'view_response.html', {'form': form, 'responses': response_data})


@login_required
def view_analytics(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    responses = form.responses.all()
    text_analytics = {}
    for question in form.questions.filter(question_type='text'):
        answers = Answer.objects.filter(question=question).values('answer_text')
        
        word_count = {}
        for answer in answers:
            for word in answer['answer_text'].split():
                    word_count[word] = word_count.get(word, 0) + 1
        
        text_analytics[question.question_text] = sorted(word_count.items(), key=lambda x: x[1], reverse=True)[:5]

    checkbox_analytics = {}
    dropdown_analytics = {}

    for question in form.questions.filter(Q(question_type='checkbox') | Q(question_type='dropdown')):
        answers = Answer.objects.filter(question=question).values('answer_text')
        option_count = {}

        for answer in answers:
            options = answer['answer_text'].split(',')
            for option in options:
                option = option.strip()
                option_count[option] = option_count.get(option, 0) + 1
        
        if question.question_type == 'checkbox':
            checkbox_analytics[question.question_text] = sorted(option_count.items(), key=lambda x: x[1], reverse=True)[:5]
        
        elif question.question_type == 'dropdown':
            dropdown_analytics[question.question_text] = sorted(option_count.items(), key=lambda x: x[1], reverse=True)[:5]

    analytics_data = {
        'total_responses': responses.count(),
        'text_analytics': text_analytics,
        'checkbox_analytics': checkbox_analytics,
        'dropdown_analytics': dropdown_analytics
    }

    return render(request, 'view_analytics.html', {'form': form, 'analytics': analytics_data})

def respond_to_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    questions = form.questions.order_by('order') 

    if request.method == 'POST':
        response = Response.objects.create(
            form=form,
            user="Anonymous" 
        )

        for question in questions:
            user_input = request.POST.getlist(f'question_{question.id}')

            if question.question_type in [Question.CHECKBOX]:
                for answer_text in user_input:
                    Answer.objects.create(
                        response=response,
                        question=question,
                        answer_text=answer_text
                    )
            else:
                Answer.objects.create(
                    response=response,
                    question=question,
                    answer_text=user_input[0] if user_input else None
                )

        return redirect('thank_you')

    return render(request, 'respond_to_form.html', {
        'form': form,
        'questions': questions,
    })

@csrf_exempt
def submit_response(request, form_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = data.get('user', 'Anonymous')
            answers = data.get('answers', [])

            form = get_object_or_404(Form, id=form_id)

            response = Response.objects.create(form=form, user=user)

            for answer_data in answers:
                question_id = answer_data['question_id']
                answer_text = answer_data.get('answer_text')

                question = get_object_or_404(Question, id=question_id)

                Answer.objects.create(
                    response=response,
                    question=question,
                    answer_text=answer_text
                )

            return JsonResponse({'redirect': '/thank-you/'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def view_form(request, form_id):
    form = get_object_or_404(Form, id=form_id)
    questions = form.questions.prefetch_related('options').order_by('order')

    return render(request, 'form_view.html', {
        'form': form,
        'questions': questions,
    })


def thank_you(request):
    return render(request, 'thank_you.html')
