from django.core.management.base import BaseCommand
from datetime import datetime
from admin_management.models import StudentData
from random import randint


subject = ['Maths', 'English', 'Malayalam', 'Physics', 'Chemistry', 'Biology']

student = [('Bruno Mars', 1, 'Stanford University'),
            ('Micheal Jackson', 1, 'University of California--Berkeley'),
            ('Madonna', 1, 'University of Oxford'),
            ('John Mayer', 2, 'Columbia University'),
            ('Will I Am', 2, 'California Institute of Technology'),
            ('Pharrel Williams', 2, 'University of Washington'),
            ('Max Martin', 3, 'University of Cambridge'),
            ('Billie Eilish', 3, 'Johns Hopkins University.'),
            ('Hans Zimmer', 3, 'University of Wales'),
            ('Britney Spears', 4, 'Massachusetts Institute of Technology'),

            ('Ricky Martin', 4, 'Stanford University'),
            ('Enrique Iglesias', 4, 'University of California--Berkeley'),
            ('Mick Jagger', 5, 'University of Oxford'),
            ('Carlos Santana', 5, 'Columbia University'),
            ('Lady Gaga', 5, 'California Institute of Technology'),
            ('Beyonce', 6, 'University of Washington'),
            ('Rihanna', 6, 'University of Cambridge'),
            ('Miley Cyrus', 6, 'Johns Hopkins University.'),
            ('Demi Lavato', 7, 'University of Wales'),
            ('Charlie Puth', 7, 'Massachusetts Institute of Technology'),

            ('Mariah Carey', 7, 'Stanford University'),
            ('Jennifer Lopez', 8, 'University of California--Berkeley'),
            ('Luis Fonsi', 8, 'University of Oxford'),
            ('Lana Del Rey', 8, 'Columbia University'),
            ('Chris Martin', 9, 'California Institute of Technology'),
            ('Selena Gomez', 9, 'University of Washington'),
            ('Dua Lipa', 9, 'University of Cambridge'),
            ('Taylor Swift', 10, 'Johns Hopkins University.'),
            ('Justin Bieber', 10, 'University of Wales'),
            ('Adele', 10, 'Massachusetts Institute of Technology'),
            ]


class Command(BaseCommand):
    
    def handle(self, *args, **options):
        current_date = datetime.today().date()
    for sh in student:    
        for sub in subject:
            for tr in range(1, 31):
                school = sh[2],
                student = sh[0],
                standard = sh[1], 
                term = tr
                mark = randint(1, 101)
                print(mark, term, standard, sh[1], sh)
                StudentData.objects.create(school=sh[2], 
                                            student=sh[0], 
                                            standard=sh[1],
                                            subject=sub, 
                                            term=term, 
                                            mark=mark)