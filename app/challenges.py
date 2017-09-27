from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.forms import QuestionsForm
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

            if action == 'add_question':
                challenge = Challenges.objects.get(pk=int(request.POST['id']))
                f = QuestionsForm(request.POST)
                if f.is_valid():
                    try:
                        with transaction.atomic():

                            question = Questions(challenge=challenge,
                                                 order=f.cleaned_data['order'],
                                                 text=f.cleaned_data['text'],
                                                 counter_time=f.cleaned_data['counter_time'],
                                                 # Answers
                                                 answer1=f.cleaned_data['answer1'],
                                                 answer2=f.cleaned_data['answer2'],
                                                 answer3=f.cleaned_data['answer3'],
                                                 answer4=f.cleaned_data['answer4'],
                                                 is_correct_answer1=f.cleaned_data['is_correct_answer1'],
                                                 is_correct_answer2=f.cleaned_data['is_correct_answer2'],
                                                 is_correct_answer3=f.cleaned_data['is_correct_answer3'],
                                                 is_correct_answer4=f.cleaned_data['is_correct_answer4'])
                            question.save()

                            return ok_json(data={'redirect_url': '/challenges',
                                                 'msg': 'You have successfully added a Question.'})
                    except Exception:
                        return bad_json(error=2)
                else:
                    return bad_json(message="Form is not valid.")
            #
            # if action == 'delete':
            #     project = Projects.objects.get(pk=int(request.POST['id']))
            #     try:
            #         with transaction.atomic():
            #             project.delete()
            #             return ok_json(data={'redirect_url': '/challenges',
            #                                  'msg': 'You have successfully deleted the PROJECT.'})
            #     except Exception:
            #         return bad_json(error=3)

        return bad_json(error=0)

    else:

        if 'action' in request.GET:
            if 'action' in request.GET:
                action = request.GET['action']

                if action == 'add_question':
                    try:
                        data['title'] = 'New Question'
                        data['challenge'] = Challenges.objects.get(pk=request.GET['id'])
                        data['form'] = QuestionsForm()
                        return render(request, 'challenges/add.html', data)
                    except Exception:
                        pass
                #
                # if action == 'edit':
                #     try:
                #         data['title'] = 'Edit Project'
                #         data['project'] = project = Projects.objects.get(pk=request.GET['id'])
                #         data['form'] = ProjectsForm(initial={'name': project.name})
                #         return render(request, 'challenges/edit.html', data)
                #     except Exception:
                #         pass
                #
                # if action == 'delete':
                #     try:
                #         data['title'] = 'Delete Project'
                #         data['project'] = Projects.objects.get(pk=request.GET['id'])
                #         data['is_delete'] = True
                #         return render(request, 'challenges/delete.html', data)
                #     except Exception:
                #         pass

            return HttpResponseRedirect('/teach')

        else:

            data['challenges'] = Challenges.objects.all()
            return render(request, 'challenges/view.html', data)
