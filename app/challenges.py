from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from app.functions import bad_json, ok_json, generate_code
from app.models import Challenges


def views(request):
    data = {'title': 'Challenges'}

    if request.method == 'POST':
        if 'action' in request.POST:
            action = request.POST['action']

            if action == 'create_challenge':
                try:
                    with transaction.atomic():

                        challenge_name = request.POST['challenge_name']
                        if Challenges.objects.filter(name=challenge_name).exists():
                            return bad_json(message="Challenge Name already exists. "
                                                    "Please change the name of the challenge and try again. ")

                        new_code = generate_code()
                        challenge = Challenges(name=challenge_name, code=new_code)
                        challenge.save()
                        return ok_json(data={'redirect_url': '/challenges',
                                             'msg': 'You have successfully created a new Challenge.'})
                except Exception as ex:
                    return bad_json(error=1)
            #
            # if action == 'edit':
            #     project = Projects.objects.get(pk=int(request.POST['id']))
            #     f = ProjectsForm(request.POST)
            #     if f.is_valid():
            #         try:
            #             with transaction.atomic():
            #
            #                 if Projects.objects.filter(name=f.cleaned_data['name']).exclude(id=project.id).exists():
            #                     return bad_json(message="Project already exists. "
            #                                             "Please change the name of the project and try again. ")
            #                 project.name = f.cleaned_data['name']
            #                 project.save()
            #                 return ok_json(data={'redirect_url': '/challenges',
            #                                      'msg': 'You have successfully edited the PROJECT.'})
            #         except Exception:
            #             return bad_json(error=2)
            #     else:
            #         return bad_json(message="Form is not valid.")
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

                # if action == 'add':
                #     try:
                #         data['title'] = 'New Project'
                #         data['form'] = ProjectsForm()
                #         return render(request, 'challenges/add.html', data)
                #     except Exception:
                #         pass
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
