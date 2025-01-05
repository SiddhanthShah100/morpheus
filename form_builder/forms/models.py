from django.db import models


class Form(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Question(models.Model):
    TEXT = 'text'
    DROPDOWN = 'dropdown'
    CHECKBOX = 'checkbox'
    RANKING = 'ranking'
    LINEAR_SCALE = 'linear_scale'
    DATE_PICKER = 'date_picker'
    TIME_PICKER = 'time_picker'
    FILE_UPLOAD = 'file_upload'
    MATRIX_GRID = 'matrix_grid'
    IMAGE_CHOICE = 'image_choice'
    SLIDER = 'slider'
    SIGNATURE_CAPTURE = 'signature_capture'
    COLOR_PICKER = 'color_picker'
    GEOLOCATION = 'geolocation'
    PERCENTAGE_ALLOCATION = 'percentage_allocation'

    QUESTION_TYPES = [
        (TEXT, 'Text'),
        (DROPDOWN, 'Dropdown'),
        (CHECKBOX, 'Checkbox'),
        (RANKING, 'Ranking'),
        (LINEAR_SCALE, 'Linear Scale'),
        (DATE_PICKER, 'Date Picker'),
        (TIME_PICKER, 'Time Picker'),
        (FILE_UPLOAD, 'File Upload'),
        (MATRIX_GRID, 'Matrix/Grid'),
        (IMAGE_CHOICE, 'Image Choice'),
        (SLIDER, 'Slider'),
        (SIGNATURE_CAPTURE, 'Signature Capture'),
        (COLOR_PICKER, 'Color Picker'),
        (GEOLOCATION, 'Geolocation'),
        (PERCENTAGE_ALLOCATION, 'Percentage Allocation'),
    ]

    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    question_text = models.CharField(max_length=255)
    question_type = models.CharField(choices=QUESTION_TYPES, max_length=50)
    order = models.PositiveIntegerField()
    min_value = models.IntegerField(null=True, blank=True)
    max_value = models.IntegerField(null=True, blank=True)
    is_required = models.BooleanField(default=True)

    options = models.JSONField(null=True, blank=True)
    matrix_rows = models.JSONField(null=True, blank=True)
    matrix_columns = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'forms_question'
        ordering = ['order']

    def __str__(self):
        return self.question_text

    def is_slider(self):
        return self.question_type == self.SLIDER

    def is_dropdown_or_checkbox(self):
        return self.question_type in [self.DROPDOWN, self.CHECKBOX, self.IMAGE_CHOICE]

    def is_matrix(self):
        return self.question_type == self.MATRIX_GRID

    def get_options(self):
        if self.is_dropdown_or_checkbox():
            return self.options
        elif self.is_matrix():
            return {
                'rows': self.matrix_rows,
                'columns': self.matrix_columns
            }
        elif self.is_slider():
            return {'min_value': self.min_value, 'max_value': self.max_value}
        return None


class Option(models.Model):
    question = models.ForeignKey(Question, related_name='option_choices', on_delete=models.CASCADE)
    option_text = models.CharField(max_length=255)

    def __str__(self):
        return self.option_text


class Response(models.Model):
    form = models.ForeignKey(Form, related_name='responses', on_delete=models.CASCADE)
    user = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Response for {self.form.title} by {self.user}'


class Answer(models.Model):
    response = models.ForeignKey(Response, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer_text = models.TextField(null=True, blank=True)
    file_upload = models.FileField(upload_to='answers/', null=True, blank=True)
    image_choice = models.ImageField(upload_to='image_choices/', null=True, blank=True)
    slider_value = models.IntegerField(null=True, blank=True)
    ranking_value = models.IntegerField(null=True, blank=True)
    geolocation_value = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'forms_answer'

    def __str__(self):
        return f'Answer to {self.question.question_text}'

    def get_answer(self):
        if self.answer_text:
            return self.answer_text
        elif self.file_upload:
            return self.file_upload.url if self.file_upload else None
        elif self.image_choice:
            return self.image_choice.url if self.image_choice else None
        elif self.slider_value is not None:
            return self.slider_value
        elif self.ranking_value is not None:
            return self.ranking_value
        elif self.geolocation_value:
            return self.geolocation_value
        return None
