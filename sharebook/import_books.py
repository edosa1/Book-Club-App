import os
import csv
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sharebook.settings')

django.setup()


from pages.models import Book

def import_books_from_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            
            bookImage = row['bookImage']
            bookTitle = row['bookTitle']
            bookAuthors = row['bookAuthors']
            bookDesc = row['bookDesc']

            # Create Book object
            Book.objects.create(
                bookImage=bookImage,
                bookTitle=bookTitle,
                bookAuthors=bookAuthors,
                bookDesc=bookDesc,

            )

if __name__ == '__main__':
    csv_file_path = "C:\\Users\\eosar\\Downloads\\Bookscopy.csv"
    import_books_from_csv(csv_file_path)