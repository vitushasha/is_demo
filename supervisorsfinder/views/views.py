from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from ..forms import SelectUserForm
from django.shortcuts import render


@main_auth(on_cookies=True)
def main_find(request):
    but = request.bitrix_user_token
    departments_dict = get_departments_dict(but)
    user_dict = get_user_dict(but)
    supervisorsinfo = {}
    if request.method == 'POST':

        form = SelectUserForm(request.POST)
        if form.is_valid():

            user = form.cleaned_data["user"]
            if user:
                user_id = user
                find_supervisors_for_users(user_dict, user_id, departments_dict)
                for department in user_dict[user_id]['UF_DEPARTMENT']:
                    department = str(department)
                    for supervisor in user_dict[user_id]['SUPERVISORS']:
                        if departments_dict[department]['UF_HEAD'] in supervisor:
                            supervisor_id = departments_dict[department]['UF_HEAD']
                            supervisorsinfo.setdefault(user_dict[user_id]['FULL_NAME'], [])
                            supervisorsinfo[user_dict[user_id]['FULL_NAME']].append({'department_name': departments_dict[department]['NAME'], 'supervisor_name': user_dict[supervisor_id]['FULL_NAME']})

                return render(request, 'supervisorsfinder.html', {'info': supervisorsinfo})

            else:
                for user_id in user_dict:
                    find_supervisors_for_users(user_dict, user_id, departments_dict)
                    for department in user_dict[user_id]['UF_DEPARTMENT']:
                        department = str(department)
                        for supervisor in user_dict[user_id]['SUPERVISORS']:
                            if departments_dict[department]['UF_HEAD'] in supervisor:
                                supervisor_id = departments_dict[department]['UF_HEAD']
                                supervisorsinfo.setdefault(user_dict[user_id]['FULL_NAME'], [])
                                supervisorsinfo[user_dict[user_id]['FULL_NAME']].append({'department_name': departments_dict[department]['NAME'], 'supervisor_name': user_dict[supervisor_id]['FULL_NAME']})

                return render(request, 'supervisorsfinder.html', {'info': supervisorsinfo})

    form = SelectUserForm()
    return render(request, 'supervisorsfinder.html', {'form': form})




def get_user_dict(but):
    users = but.call_list_method('user.get')
    user_fields = ['ID', 'NAME', 'LAST_NAME', 'SECOND_NAME', 'UF_DEPARTMENT']
    user_dict = {}
    for element in users:
        user_dict.update({element['ID']: {}})
        for field in user_fields:
            try:
                user_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass
        user_dict[element['ID']].pop('ID')
        for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
            try:
                user_dict[element['ID']].setdefault("FULL_NAME", '')
                user_dict[element['ID']]['FULL_NAME'] += user_dict[element['ID']][key] + " "
            except KeyError:
                pass
    return user_dict

def get_departments_dict(but):
    departments = but.call_list_method('department.get')
    departments_fields = ['ID', 'NAME', 'SORT', 'PARENT', 'UF_HEAD']
    department_dict = {}
    for element in departments:
        department_dict.update({element['ID']: {}})
        for field in departments_fields:
            try:
                department_dict[element['ID']].update({field: element[field]})
            except KeyError:
                pass
        department_dict[element['ID']].pop('ID')
    return department_dict

def find_supervisors_for_users(user_dict, user_id, departments_dict):
    user = user_dict[user_id]
    # Руководителей записываем в сет, чтобы не искать дубликаты.
    user.update({'SUPERVISORS': set()})
    for department_id in departments_dict:
        #  Смотрим, состоит ли человек в текущем подразделении.
        #  Если состоит, то в качестве кого?
        if departments_dict[department_id].get('UF_HEAD') == user_id:
            if "PARENT" in departments_dict[department_id]:
                department = departments_dict[department_id]['PARENT']
                supervisor_id, order = find_supervisor(departments_dict, department, order=1)
            else:
                supervisor_id = "None"

        else:
            if int(department_id) in user['UF_DEPARTMENT']:
                department = department_id
                supervisor_id, order = find_supervisor(departments_dict, department)
            else:
                continue
        #  В функцию поиска передается родительское подразделение, если в текущем
        #   юзер является руководителем. В ином случае передается текущее.

        if supervisor_id != "None":
            supervisor = user_dict[supervisor_id]
            conj_str = ""
            for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
                try:
                    conj_str += f'{supervisor[key]} '
                except KeyError:
                    pass
            conj_str += f"| ID: {supervisor_id} | Порядок: {order}"
            user['SUPERVISORS'].add((supervisor_id, conj_str))
    if user['SUPERVISORS'] == set():
        user['SUPERVISORS'] = ""


def find_supervisor(departments_dict, current_dep='1', order=0):
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        return department['UF_HEAD'], order
    else:
        if not parent_exists:
            return "None", order
        return find_supervisor(departments_dict, department['PARENT'], order + 1)