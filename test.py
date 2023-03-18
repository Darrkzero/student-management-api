# TCXP9bwKjg  sinzu

# nrW-Tetx{^ jude

# SSFx-lG-cQ eze

# iH:--y#+53 toni

# T\\.`2~]#^u chi

courses = [60,70,80,60,90,90]
total_grade_points = 0
for course in courses:
    if course >= 90:
        total_grade_points += 4.0
    elif course >= 80:
        total_grade_points += 3.0
    elif course >= 70:
        total_grade_points += 2.0
    elif course >= 60:
        total_grade_points += 1.0
    else:
        total_grade_points += 0.0
gpa = total_grade_points / len(courses)

print(gpa)