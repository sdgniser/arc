# Django script to add all courses and items from data/SDG_NISER/*/*
# Run this in `python manage.py shell` or as a Django management command

import os
import re
from django.core.files import File
from django.utils import timezone
from main.models import School, Course, Itr, Item
from authtools.models import User

# Set operator user
op = User.objects.get(email="shithij.t@niser.ac.in")

# Path to the data root
base_dir = "data/SDG_NISER"

# Regex for <Course_Code>_<course_name_in_snake_case>
course_pattern = re.compile(r"^([A-Za-z0-9]+)_(.+)$")

# Fixed regex pattern for files
# Matches: coursecode_itemname_year.pdf, coursecode_itemname_year_.pdf, etc.
# Examples: b202_endsem_2016.pdf, b202_endsem_2021_.pdf, b202_quiz_1_2021.pdf
file_pattern = re.compile(r"^([a-z0-9]+)_(.+?)_(\d{4})_?\.pdf$", re.IGNORECASE)

print("Starting course and item import...")

for school in School.objects.all():
    school_dir = os.path.join(base_dir, school.abbr)
    if not os.path.isdir(school_dir):
        print(f"Skipping {school.abbr}: directory not found")
        continue
    
    print(f"\nProcessing school: {school.abbr}")
    
    for course_dir in os.listdir(school_dir):
        course_match = course_pattern.match(course_dir)
        if not course_match:
            print(f"  Skipping directory {course_dir}: doesn't match course pattern")
            continue
            
        code = course_match.group(1).upper()  # Convert to uppercase for consistency
        if len(code) > 6:
            print(f"  Skipping {course_dir}: code '{code}' too long for Course.code field")
            continue
            
        name_snake = course_match.group(2)
        name = name_snake.replace("_", " ").title()  # Better capitalization
        
        # Get or create course
        course, created = Course.objects.get_or_create(
            code=code,
            school=school,
            defaults={"op": op, "name": name, "appr": True}
        )
        
        if created:
            print(f"  Created course: {course}")
        else:
            print(f"  Found existing course: {course}")
        
        full_course_dir = os.path.join(school_dir, course_dir)
        
        # Pass 1: Collect all years from files and create iterations
        years_found = set()
        valid_files = []
        
        for fname in os.listdir(full_course_dir):
            if not fname.lower().endswith('.pdf'):
                print(f"    Skipping non-PDF: {fname}")
                continue
                
            file_match = file_pattern.match(fname)
            if not file_match:
                print(f"    Skipped (regex mismatch): {fname}")
                continue
                
            file_code = file_match.group(1).upper()
            item_name_raw = file_match.group(2)
            year = file_match.group(3)
            
            if file_code != code:
                print(f"    Skipped (code mismatch): {file_code} != {code} for {fname}")
                continue
            
            years_found.add(year)
            valid_files.append((fname, file_code, item_name_raw, year))
            
        print(f"    Found years: {sorted(years_found)}")
        
        # Create all iterations for this course
        for year in years_found:
            itr, created = Itr.objects.get_or_create(
                course=course,
                year=year,
                defaults={
                    "op": op, 
                    "appr": True,
                    "sem": "FA",  # Default to Fall semester
                    "inst": "Unknown"  # Default instructor
                }
            )
            if created:
                print(f"    Created iteration: {itr}")
        
        # Pass 2: Add items to each iteration
        for fname, file_code, item_name_raw, year in valid_files:
            # Clean up item name
            item_name = item_name_raw.replace("_", " ").replace("-", " ").strip()
            item_name = " ".join(word.capitalize() for word in item_name.split())
            
            itr = Itr.objects.get(course=course, year=year)
            
            # Check if item already exists
            if Item.objects.filter(itr=itr, name=item_name).exists():
                print(f"    Skipped existing item: {item_name} in {itr}")
                continue
            
            # Create the item
            src_path = os.path.join(full_course_dir, fname)
            try:
                with open(src_path, "rb") as f:
                    django_file = File(f, name=fname)
                    item = Item(
                        op=op,
                        itr=itr,
                        name=item_name,
                        appr=True,
                        time=timezone.now(),
                        desc=f"Imported from {fname}"
                    )
                    # Save the file to the model
                    item.fl.save(fname, django_file, save=False)
                    item.save()
                    
                print(f"    ✓ Added item: {item_name} to {itr}")
                
            except Exception as e:
                print(f"    ✗ Error adding {fname}: {str(e)}")

print("\n✅ Import completed!")

# Print summary
total_courses = Course.objects.count()
total_itrs = Itr.objects.count()
total_items = Item.objects.count()

print(f"\nSummary:")
print(f"Total Courses: {total_courses}")
print(f"Total Iterations: {total_itrs}")
print(f"Total Items: {total_items}")