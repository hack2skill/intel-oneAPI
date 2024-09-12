from django.db import models

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    favourite_categories = models.JSONField(default=list)
    rank = models.PositiveIntegerField(null=True, blank=True)
    class_rank = models.PositiveIntegerField(null=True, blank=True)
    section_rank = models.PositiveIntegerField(null=True, blank=True)  
    pet_rank = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.student_name

    def update_pet_rank(self):
        students = Student.objects.order_by(
            '-pet__pet_level',
            '-pet__pet_progress'
        )
        pet_rank = 1
        for index, student in enumerate(students):
            student.pet_rank = pet_rank
            student.save()
            if student.id == self.id:
                self.pet_rank = pet_rank
            pet_rank += 1
        self.save()

    def update_rank(self):
        students = Student.objects.order_by(
            '-marks__average_marks',
            '-attendance__average_attendance',
            '-assignment__assignment_percentage'
        )
        rank = 1
        class_students = students.filter(class_name=self.class_name)
        section_students = class_students.filter(section=self.section)  # Filter students by section

        for index, student in enumerate(students):
            student.rank = rank
            student.save()
            if student.id == self.id:
                self.rank = rank
            rank += 1

        class_rank = 1
        for index, student in enumerate(class_students):
            student.class_rank = class_rank
            student.save()
            if student.id == self.id:
                self.class_rank = class_rank
            class_rank += 1

        section_rank = 1
        for index, student in enumerate(section_students):
            student.section_rank = section_rank
            student.save()
            if student.id == self.id:
                self.section_rank = section_rank
            section_rank += 1

        self.save()

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    maths = models.PositiveIntegerField()
    hindi = models.PositiveIntegerField()
    english = models.PositiveIntegerField()
    science = models.PositiveIntegerField()
    social_science = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField(default=0)
    average_marks = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.update_total_marks()
        self.update_average_marks()
        super().save(*args, **kwargs)
        self.student.update_rank()

    def update_total_marks(self):
        self.total_marks = self.maths + self.hindi + self.english + self.science + self.social_science

    def update_average_marks(self):
        total_subjects = 5  # Assuming 5 subjects in total
        self.average_marks = self.total_marks / total_subjects

    def __str__(self):
        return f"{self.student.student_name}'s Marks"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    maths_attendance = models.PositiveIntegerField()
    hindi_attendance = models.PositiveIntegerField()
    english_attendance = models.PositiveIntegerField()
    science_attendance = models.PositiveIntegerField()
    social_science_attendance = models.PositiveIntegerField()
    average_attendance = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.update_average_attendance()
        super().save(*args, **kwargs)
        self.student.update_rank()

    def update_average_attendance(self):
        total_subjects = 5  # Assuming 5 subjects in total
        total_attendance = (
            self.maths_attendance +
            self.hindi_attendance +
            self.english_attendance +
            self.science_attendance +
            self.social_science_attendance
        )
        self.average_attendance = (total_attendance / (total_subjects * 100)) * 100

    def __str__(self):
        return f"{self.student.student_name}'s Attendance"


class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='assignment')
    completed_assignments = models.PositiveIntegerField(default=0)
    total_assignments = models.PositiveIntegerField(default=0)
    assignment_percentage = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.update_assignment_percentage()
        super().save(*args, **kwargs)
        self.student.update_rank()

    def update_assignment_percentage(self):
        if self.total_assignments > 0:
            self.assignment_percentage = (self.completed_assignments / self.total_assignments) * 100
        else:
            self.assignment_percentage = 0

    def __str__(self):
        return f"{self.student.student_name}'s Assignments"
    
class Pet(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='pet')
    pet_name = models.CharField(max_length=100, default="\'NA\'")
    pet_type = models.CharField(max_length=100)
    pet_level = models.PositiveIntegerField(default=1)
    pet_progress = models.PositiveIntegerField(default=0)
    pet_coins = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.student.update_pet_rank()
