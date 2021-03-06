from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.functions import bad_json, ok_json, generate_code
from app.models import Challenges, Questions


def views(request):
    data = {'title': 'Challenges'}

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'create_challenge':
                try:
                    with transaction.atomic():

                        if 'challenge_name' in request.POST and request.POST['challenge_name'] != '':
                            challenge_name = request.POST['challenge_name']
                            if Challenges.objects.filter(name=challenge_name).exists():
                                return bad_json(message="Challenge Name already exists. "
                                                        "Please change the name of the challenge and try again. ")

                            new_code = generate_code()
                            challenge = Challenges(name=challenge_name, code=new_code)
                            challenge.save()
                            return ok_json(data={'message': 'Good Job!. You successfully created a new Challenge.'})

                        else:
                            return bad_json(message="Not Challenge received")

                except Exception as ex:
                    return bad_json(error=1)

            if action == 'questions':
                challenge = Challenges.objects.get(pk=int(request.POST['id']))

                question = None
                if 'qid' in request.POST and request.POST['qid'] != '':
                    question = Questions.objects.get(pk=int(request.POST['qid']))

                correct_answer = int(request.POST['q_answers_checks'])

                try:
                    with transaction.atomic():

                        if not question:

                            question = Questions(challenge=challenge,
                                                 text=request.POST['q_text'],
                                                 order=request.POST['q_order'],
                                                 answer1=request.POST['q_answer1'],
                                                 answer2=request.POST['q_answer2'],
                                                 answer3=request.POST['q_answer3'],
                                                 answer4=request.POST['q_answer4'],
                                                 is_correct_answer1=True if correct_answer == 1 else False,
                                                 is_correct_answer2=True if correct_answer == 2 else False,
                                                 is_correct_answer3=True if correct_answer == 3 else False,
                                                 is_correct_answer4=True if correct_answer == 4 else False)

                        else:

                            question.text = request.POST['q_text']
                            question.order = request.POST['q_order']
                            question.counter_time = request.POST['q_counter']

                            question.answer1 = request.POST['q_answer1']
                            question.answer2 = request.POST['q_answer2']
                            question.answer3 = request.POST['q_answer3']
                            question.answer4 = request.POST['q_answer4']
                            question.is_correct_answer1 = True if correct_answer == 1 else False
                            question.is_correct_answer2 = True if correct_answer == 2 else False
                            question.is_correct_answer3 = True if correct_answer == 3 else False
                            question.is_correct_answer4 = True if correct_answer == 4 else False

                        question.save()

                        return ok_json(data={'redirect_url': '/challenges',
                                             'message': 'Successfully {} a Question'.format('Created' if not question else 'Edited')})

                except Exception:
                    return bad_json(message="Error saving data")

            if action == 'delete_question':
                try:
                    question = Questions.objects.get(pk=int(request.POST['qid']))
                    with transaction.atomic():
                        if question.responses_set.exists():
                            question.responses_set.all().delete()
                        question.delete()
                        return ok_json(data={'redirect_url': '/challenges',
                                             'message': 'Successfully Deleted the Question.'})
                except Exception:
                    return bad_json(message="Error deleting Question")

            if action == 'access_challenge':
                try:
                    code = request.POST['code']
                    if not Challenges.objects.filter(code=code).exists():
                        return bad_json(message='Code does not exist in the system.')

                    return ok_json(data={'challengeID': Challenges.objects.filter(code=code)[0].id})

                except Exception:
                    return bad_json(message='Error getting data')

            if action == 'response_question':
                question = Questions.objects.get(pk=int(request.POST['qid']))
                response = int(request.POST['response'])

                if response == 1 and question.is_correct_answer1:
                    return ok_json()

                elif response == 2 and question.is_correct_answer2:
                    return ok_json()

                elif response == 3 and question.is_correct_answer3:
                    return ok_json()

                elif response == 4 and question.is_correct_answer4:
                    return ok_json()

                else:
                    return bad_json(message='INCORRECT')

        return bad_json(message="Bad Request")

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'questions':
                    try:
                        data['title'] = 'New Question'
                        data['challenge'] = Challenges.objects.get(pk=request.GET['id'])
                        question = None
                        if 'qid' in request.GET and request.GET['qid'] != '':
                            question = Questions.objects.get(pk=int(request.GET['qid']))
                        data['question'] = question
                        return render(request, 'challenges/questions.html', data)
                    except Exception:
                        pass

                if action == 'play':
                    try:
                        data['title'] = 'Play Challenge'
                        data['challenge'] = challenge = Challenges.objects.get(pk=request.GET['id'])
                        data['questions'] = questions = challenge.get_my_questions()
                        data['first_question'] = questions[0]
                        data['current_question'] = questions[0]
                        return render(request, 'challenges/play.html', data)
                    except Exception:
                        pass

            return HttpResponseRedirect('/challenges')

        data['challenges'] = Challenges.objects.all()
        return render(request, 'challenges/view.html', data)
