# Django script to add all courses and items from data/SDG_NISER/*/*
# Run this in `python manage.py shell` or as a Django management command

import os
import re
import sys
import django

# 1. Point Django to your settings module ('arc.settings')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arc.settings')

# 2. Add the project root to the system path if your script is in a subfolder
# (Adjust this path if your script lives somewhere else!)
sys.path.append('/home/ccarchive/archive/arc')

# 3. Initialize Django
django.setup()

from django.core.files import File
from django.utils import timezone
from main.models import School, Course, Itr, Item
from authtools.models import User

# Set operator user
op = User.objects.get(email="sandipan.samanta@niser.ac.in")

# Path to the data root
base_dir = "/home/ccarchive/archive/arc/staticfiles/SDG_NISER"

# print("Checking and initializing Schools...")

# SCHOOLS_DATA = {
#     "SBS": "School of Biological Sciences",
#     "SCS": "School of Chemical Sciences",
#     "SMS": "School of Mathematical Sciences",
#     "SPS": "School of Physical Sciences",
#     "SEPS": "School of Earth and Planetary Sciences",
#     "SCoS": "School of Computer Sciences",
#     "SHSS": "School of Humanities and Social Sciences",
#     "CMRP": "Centre for Medical and Radiation Physics"
# }

# for abbr, full_name in SCHOOLS_DATA.items():
#     # If your School model requires the 'op' or 'appr' fields like your Course model does, 
#     # add them to the defaults dictionary below.
#     school, created = School.objects.get_or_create(
#         abbr=abbr,
#         defaults={"name": full_name}
#     )
#     if created:
#         print(f"  + Created new school: {abbr} - {full_name}")

# Regex for <Course_Code>_<course_name_in_snake_case>
course_pattern = re.compile(r"^([A-Za-z0-9]+)_(.+)$")

# Fixed regex pattern for files
# Matches: coursecode_itemname_year.pdf, coursecode_itemname_year_.pdf, etc.
# Examples: b202_endsem_2016.pdf, b202_endsem_2021_.pdf, b202_quiz_1_2021.pdf
# file_pattern = re.compile(r"^([a-z0-9]+)_(.+?)_(\d{4})_?\.pdf$", re.IGNORECASE)
# A list of patterns to try, from most specific to least specific
FILE_PATTERNS = [
    # 1. Standard (Code, Item, Year): b202_endsem_2021.pdf, b202-quiz 1-2021_sol.pdf
    re.compile(r"^([a-z0-9]+)[_\-\s]+(.+?)[_\-\s]+(\d{4}).*\.pdf$", re.IGNORECASE),
    
    # 2. Year at the front (Year, Code, Item): 2021_b202_endsem.pdf
    re.compile(r"^(\d{4})[_\-\s]+([a-z0-9]+)[_\-\s]+(.+)\.pdf$", re.IGNORECASE),
    
    # 3. No Year included (Code, Item): b202_endsem.pdf
    re.compile(r"^([a-z0-9]+)[_\-\s]+(.+)\.pdf$", re.IGNORECASE)
]

# ==========================================
# File Tracking Statistics
# ==========================================
stats = {
    "total_seen": 0,
    "added": 0,
    "skipped_existing": 0,
    "skipped_regex": 0,
    "skipped_non_pdf": 0,
    "skipped_mismatch": 0,
    "errors": 0
}

print("\nStarting course and item import...")

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
            stats["total_seen"] += 1  # Count every file we look at
            
            if not fname.lower().endswith('.pdf'):
                print(f"    Skipping non-PDF: {fname}")
                stats["skipped_non_pdf"] += 1
                continue
            
            file_code = None
            item_name_raw = None
            year = None

            # (Assuming you are using the updated FILE_PATTERNS list from earlier)
            match = FILE_PATTERNS[0].match(fname)
            if match:
                file_code, item_name_raw, year = match.groups()
            elif FILE_PATTERNS[1].match(fname):
                match = FILE_PATTERNS[1].match(fname)
                year, file_code, item_name_raw = match.groups()
            elif FILE_PATTERNS[2].match(fname):
                match = FILE_PATTERNS[2].match(fname)
                file_code, item_name_raw = match.groups()
                year = "0000" 
            
            if not file_code:
                print(f"    ⚠️ UNMATCHED FORMAT, SKIPPING: {fname}")
                stats["skipped_regex"] += 1
                continue
                
            file_code = file_code.upper()
            
            if file_code != code:
                print(f"    Skipped (code mismatch): {file_code} != {code} for {fname}")
                stats["skipped_mismatch"] += 1
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
            item_name = item_name_raw.replace("_", " ").replace("-", " ").strip()
            item_name = " ".join(word.capitalize() for word in item_name.split())
            
            itr = Itr.objects.get(course=course, year=year)
            
            # Check if item already exists
            if Item.objects.filter(itr=itr, name=item_name).exists():
                print(f"    Skipped existing item: {item_name} in {itr}")
                stats["skipped_existing"] += 1
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
                    item.fl.save(fname, django_file, save=False)
                    item.save()
                    
                print(f"    ✓ Added item: {item_name} to {itr}")
                stats["added"] += 1  # Track success!
                
            except Exception as e:
                print(f"    ✗ Error adding {fname}: {str(e)}")
                stats["errors"] += 1  # Track errors

print("\n✅ Import completed!")

print(f"\n{'='*50}")
print(" 📊 IMPORT EXECUTION SUMMARY")
print(f"{'='*50}")
print(f"Total Files Scanned in Folders:  {stats['total_seen']}")
print(f"  ✓ Successfully Added to DB:    {stats['added']}")
print(f"  ⏭ Skipped (Already in DB):     {stats['skipped_existing']}")
print(f"  ⏭ Skipped (Not a PDF file):    {stats['skipped_non_pdf']}")
print(f"  ⚠️ Skipped (Unmatched Regex):   {stats['skipped_regex']}")
print(f"  ⚠️ Skipped (Folder Mismatch):   {stats['skipped_mismatch']}")
print(f"  ❌ Errors during upload:       {stats['errors']}")
print(f"{'-'*50}")
print(" 🗄️ CURRENT DATABASE TOTALS")
print(f"{'-'*50}")
print(f"Total Courses:    {Course.objects.count()}")
print(f"Total Iterations: {Itr.objects.count()}")
print(f"Total Items:      {Item.objects.count()}")
print(f"{'='*50}\n")