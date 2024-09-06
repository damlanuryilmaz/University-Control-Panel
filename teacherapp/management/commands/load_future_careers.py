from sklearn.preprocessing import LabelEncoder, OneHotEncoder, Normalizer
from sklearn.model_selection import train_test_split
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from teacherapp.models import CareerSuggestion
import pandas as pd
import joblib
import csv


class Command(BaseCommand):
    help = 'Load recommendations from a csv file'

    def handle(self, *args, **kwargs):
        self.train_and_save_model()

    def save_model(self):
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
                    suggested_career=row[38],
                )
        self.stdout.write(self.style.SUCCESS('Careers loaded successfully!'))

    def train_and_save_model(self):
        data = CareerSuggestion.objects.all().values()
        df = pd.DataFrame(data)

        normalize_columns = [
            'operating_sys_percentage',
            'algorithms_percentage',
            'programming_percentage',
            'software_eng_percentage',
            'computer_network_percentage',
            'electronics_percentage',
            'computer_arc_percentage',
            'math_percentage',
            'communication_skills_percentage',
            'coding_skills'
        ]

        # Prepare features and target
        X = df[normalize_columns]
        y = df['suggested_career']

        # Label encoding for target variable
        label_encoder = LabelEncoder()
        y_encoded = label_encoder.fit_transform(y)

        # Normalization
        normalizer = Normalizer()
        X_normalized = normalizer.fit_transform(X)

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_normalized, y_encoded, test_size=0.2, random_state=42)

        # Train model
        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        # Initialize and train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Save model and encoders
        joblib.dump(model, 'static/models/career_suggestion_model.pkl')
        joblib.dump(normalizer, 'static/models/normalizer.pkl')
        joblib.dump(label_encoder, 'static/models/label_encoder.pkl')

        self.stdout.write(self.style.SUCCESS(
            'Model and encoders saved successfully!'))
