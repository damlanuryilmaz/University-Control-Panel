from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Normalizer
from sklearn.model_selection import train_test_split
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from teacherapp.models import CareerSuggestion
import pandas as pd
import joblib
import csv
import io


class Command(BaseCommand):
    help = 'Load recommendations from a csv file'

    def handle(self, *args, **kwargs):
        with open('static/data/future_career.csv', 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header
            for row in reader:
                CareerSuggestion.objects.create(
                    operating_sys_percentage=row[0],
                    algorithms_percentage=row[1],
                    programming_percentage=row[2],
                    software_eng_percentage=row[3],
                    computer_network_percentage=row[4],
                    electronics_percentage=row[5],
                    computer_arc_percentage=row[6],
                    math_percentage=row[7],
                    communication_skills_percentage=row[8],
                    coding_skills=row[12],
                    is_self_learning=row[15],
                    certificate=row[17],
                    interested_subject=row[22],
                    is_in_teams=row[36],
                    is_introvert=row[37],
                    suggested_career=row[38],
                )
        self.stdout.write(
            self.style.SUCCESS('Careers loaded successfully!')
        )

    def train_and_save_model(self):
        data = CareerSuggestion.objects.all().values()
        df = pd.DataFrame(data)

        label_encoder = LabelEncoder()

        # Categorical columns
        label_columns = [
            'is_self_learning',
            'is_in_teams',
            'is_introvert',
            'suggested_career',
            'certificate',
            'interested_subject'
        ]

        # Categorical data to numerical data
        for column in label_columns:
            df[column] = label_encoder.fit_transform(df[column])

        