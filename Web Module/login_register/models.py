from django.db import models
from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    favourite_categories = models.ManyToManyField(Category, related_name='students')

    def __str__(self):
        return self.student_name

class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
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

    def update_total_marks(self):
        self.total_marks = self.maths + self.hindi + self.english + self.science + self.social_science

    def update_average_marks(self):
        total_subjects = 5  # Assuming 5 subjects in total
        self.average_marks = self.total_marks / total_subjects

    def __str__(self):
        return f"{self.student.student_name}'s Marks"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    maths_attendance = models.PositiveIntegerField()
    hindi_attendance = models.PositiveIntegerField()
    english_attendance = models.PositiveIntegerField()
    science_attendance = models.PositiveIntegerField()
    social_science_attendance = models.PositiveIntegerField()
    average_attendance = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.update_average_attendance()
        super().save(*args, **kwargs)

    def update_average_attendance(self):
        total_subjects = 5  # Assuming 5 subjects in total
        total_attendance = self.maths_attendance + self.hindi_attendance + self.english_attendance + self.science_attendance + self.social_science_attendance
        self.average_attendance = (total_attendance / (total_subjects * 100)) * 100

    def __str__(self):
        return f"{self.student.student_name}'s Attendance"

class Assignment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    completed_assignments = models.PositiveIntegerField(default=0)
    total_assignments = models.PositiveIntegerField(default=0)
    assignment_percentage = models.FloatField(default=0)

    def save(self, *args, **kwargs):
        self.update_assignment_percentage()
        super().save(*args, **kwargs)

    def update_assignment_percentage(self):
        if self.total_assignments > 0:
            self.assignment_percentage = (self.completed_assignments / self.total_assignments) * 100
        else:
            self.assignment_percentage = 0

    def __str__(self):
        return f"{self.student.student_name}'s Assignments"

class Rank(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    average_marks = models.FloatField(default=0)
    average_attendance = models.FloatField(default=0)
    average_assignment_percent = models.FloatField(default=0)
    rank = models.IntegerField(default=0)

    def __str__(self):
        return f"Rank: {self.rank}, Student: {self.student.student_name}"

class ClassRank(models.Model):
    class_name = models.CharField(max_length=100)
    ranks = models.ManyToManyField(Rank)

    def __str__(self):
        return f"Class: {self.class_name}"

class SectionRank(models.Model):
    class_name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    ranks = models.ManyToManyField(Rank)

    def __str__(self):
        return f"Class: {self.class_name}, Section: {self.section}"

@receiver(post_save, sender=Marks)
@receiver(post_save, sender=Attendance)
@receiver(post_save, sender=Assignment)
def update_rank(sender, instance, **kwargs):
    student = instance.student
    average_marks = Marks.objects.filter(student=student).aggregate(avg_marks=Sum('average_marks')).get('avg_marks') or 0
    average_attendance = Attendance.objects.filter(student=student).aggregate(avg_attendance=Sum('average_attendance')).get('avg_attendance') or 0
    average_assignment_percent = Assignment.objects.filter(student=student).aggregate(avg_assignment=Sum('assignment_percentage')).get('avg_assignment') or 0

    # Update or create the rank for the student
    rank, _ = Rank.objects.get_or_create(student=student)
    rank.average_marks = average_marks
    rank.average_attendance = average_attendance
    rank.average_assignment_percent = average_assignment_percent
    rank.save()

    # Update the class rank
    class_rank, _ = ClassRank.objects.get_or_create(class_name=student.class_name)
    class_rank.ranks.add(rank)

    # Update the section rank
    section_rank, _ = SectionRank.objects.get_or_create(class_name=student.class_name, section=student.section)
    section_rank.ranks.add(rank)

    # Calculate and update the rank for the student
    rank.rank = Rank.objects.filter(average_marks__gt=average_marks).count() + 1
    rank.save()

    class_rank.save()
    section_rank.save()


class VirtualPet(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='virtual_pet')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=100)
    pet_level = models.PositiveIntegerField(default=1)
    pet_level_progress = models.PositiveIntegerField(default=0)
    pet_coin = models.PositiveIntegerField(default=200)
    rank = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        self.rank = VirtualPet.objects.filter(pet_level__gt=self.pet_level).count() + 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.pet_name

@receiver(post_save, sender=VirtualPet)
def update_pet_rank(sender, instance, **kwargs):
    VirtualPet.objects.filter(pk=instance.pk).update(rank=instance.rank)
