# import gspread
#
# from requests import get
#
# from app.write_log import write_log
#
#
# class ExcelConnector:
#     def __init__(self):
#
#         gc = gspread.service_account(filename='conf.json')
#
#         table = gc.open_by_url(
#             'https://docs.google.com/spreadsheets/d/1XGTMsbrI2T5p_xhmEV3afAFno3u1y9k7kWqUuzuOkrA/edit?gid=0#gid=0')
#
#         self.worksheet = table.worksheet("teachers")
#
#     def all_teachers(self):
#         try:
#             all_teachers = self.worksheet.get_all_values()[1:]
#             for i in range(len(all_teachers)):
#                 all_teachers[i][6] = int(all_teachers[i][6])
#                 all_teachers[i][8] = int(all_teachers[i][8])
#             return all_teachers
#         except Exception as e:
#             print(e)
#             return False
#
#     def search_by_subject(self, subject, teachers):
#         return [i for i in teachers if i[3].lower() == subject.lower()]
#
#     def search_by_other_subject(self, teachers, subjects):
#         return [i for i in teachers if i[3].lower() not in list(map(lambda x: x.lower(), subjects))]
#
#     def search_by_name(self, name, teachers):
#         return [i for i in teachers if i[1].lower() == name.lower()]
#
#     def search_by_surname(self, surname, teachers):
#         return [i for i in teachers if i[2].lower() == surname.lower()]
#
#     def search_by_age(self, age: int, teachers):
#         result = []
#         for teacher in teachers:
#             age_ = int(teacher[4])
#             if int(age) == age_:
#                 result.append(teacher)
#         return result
#
#     def search_by_school(self, school, teachers):
#         return [i for i in teachers if int(i[5]) == int(school)]
#
#     def search_by_tariff(self, tariff, teachers):
#         return [i for i in teachers if int(i[6]) <= tariff]
#
#     def search_by_achievements(self, achievements, teachers):
#         return [i for i in teachers if len(set(map(lambda x: ' '.join(x.split('_')).lower(), i[13].split(', '))) & set(
#             map(lambda x: ' '.join(x.split('_')).lower(), achievements)))]
#
#     def search_by_other_achievements(self, teachers, achievements):
#         return [i for i in teachers if
#                 i[13].lower() not in list(map(lambda x: ' '.join(x.split('_')).lower(), achievements))]
#
#     def search_by_hobbies(self, hobbies, teachers):
#         return [i for i in teachers if len(set(map(lambda x: ' '.join(x.split('_')).lower(), i[14].split(', '))) & set(
#             map(lambda x: ' '.join(x.split('_')).lower(), hobbies)))]
#
#     def search_by_other_hobbies(self, teachers, hobbies):
#         print(teachers[0][14])
#         print(list(map(lambda x: ' '.join(x.split('_')).lower(), hobbies)))
#         return [i for i in teachers if
#                 i[14].lower() not in list(map(lambda x: ' '.join(x.split('_')).lower(), hobbies))]
#
#     def teacher_by_id(self, id):
#         try:
#             teacher = [i for i in self.worksheet.get_all_values()[1:] if int(i[0]) == id][0]
#             teacher[0] = int(teacher[0])
#             teacher[6] = int(teacher[6])
#             teacher[8] = int(teacher[8])
#             return teacher
#         except Exception as e:
#             write_log(e)
#             return False
#
#
#     def load_images(self):
#         try:
#             teachers = self.all_teachers()
#             ids = []
#             for teacher in teachers:
#                 r = teacher[9].split('/')
#                 ids.append(r[r.index('d') + 1])
#
#             for i, id in enumerate(ids):
#                 url = f'https://drive.google.com/uc?id={id}&export=download'
#                 resp = get(url)
#                 with open(f'static/teachers_images/{i}.png', 'wb') as file:
#                     file.write(resp.content)
#         except Exception as e:
#             write_log(e)
#
#
#
#
# if __name__ == '__main__':
#     connector = ExcelConnector()
#     all_teachers = connector.all_teachers()
#     connector.load_images()
