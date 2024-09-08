
from sklearn.discriminant_analysis import StandardScaler
from sklearn.model_selection import train_test_split
from django.core.management.base import BaseCommand
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
import pandas as pd
import joblib
import csv

from teacherapp.models import FieldArea


class Command(BaseCommand):
    help = 'Load recommendations from a csv file'

    def handle(self, *args, **kwargs):
        self.train_and_save_model()

    def save_model(self, *args, **kwargs):
        file_path = 'static/data/data.csv'

        # Open and read the CSV file
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if it exists

            for row in reader:
                field_name = row[2].strip()

                # Save each field name to the database
                FieldArea.objects.get_or_create(name=field_name)

        self.stdout.write(self.style.SUCCESS(
            'Field areas imported successfully!'))

    def train_and_save_model(self):
        # Load data
        df = pd.read_csv('static/data/data.csv')

        df.isnull().sum()

        # Feature and target variables
        X = df.drop(columns=['PlacedOrNot'], axis=1)
        y = df['PlacedOrNot']

        # Define the feature columns
        numerical_features = ['Age', 'Internships',
                              'CGPA', 'Hostel', 'HistoryOfBacklogs']
        categorical_features = ['Gender', 'Field']

        # Preprocessing pipelines for numerical and categorical data
        numeric_transformer = Pipeline(steps=[
            ('scaler', StandardScaler())])

        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))])

        # Combine preprocessing steps
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', numeric_transformer, numerical_features),
                ('cat', categorical_transformer, categorical_features)])

        # Create and train the model
        model = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', RandomForestClassifier(random_state=42))])

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42)
        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        # Calculate accuracy
        accuracy = accuracy_score(y_test, predictions)
        print(f'Accuracy: {accuracy:.2f}')

        # Save the model
        joblib.dump(model, 'static/models/model.pkl')

        self.stdout.write(self.style.SUCCESS(
            'Model and encoders saved successfully!'))
