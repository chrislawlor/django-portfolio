from django.db import models

HIDDEN = 0
LIVE = 1
NEEDS_APPROVAL = 2
STATUS_CHOICES = ((HIDDEN, 'Hidden'),
                  (LIVE, 'Live'),
                  (NEEDS_APPROVAL, 'Needs Approval'))

class Project(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    url = models.URLField(blank=True, null=True)
    pull_quote = models.TextField(blank=True, null=True)
    short_description = models.TextField()
    description = models.TextField()
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    category = models.ForeignKey('Category')
    skills = models.ManyToManyField('Skill')

    class Meta:
        ordering = ['-start_date', '-end_date', ]

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.project_detail', (), {'slug': str(self.slug), })

class Skill(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.skill_detail', (), {'slug': str(self.slug), })

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50, unique=True)
    position = models.PositiveIntegerField()

    class Meta:
        ordering = ["position"]
        verbose_name_plural = 'Categories'

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('portfolio.views.category_detail', (), {'slug': str(self.slug), })

class ProjectFile(models.Model):
    project = models.ForeignKey('Project')
    file = models.FileField(upload_to="project_file/%Y/%m/%d")
    desc = models.TextField()

    def __unicode__(self):
        return self.file.name

    def get_absolute_url(self):
        return self.file.url

class ProjectImage(models.Model):
    project = models.ForeignKey('Project')
    image = models.ImageField(upload_to="project_image/%Y/%m/%d")
    desc = models.TextField()

    def __unicode__(self):
        return self.image.name

    def get_absolute_url(self):
        return self.image.url

class TestimonyManager(models.Manager):
    """
    Only return live testimonies.
    """
    def get_query_set(self):
        return super(TestimonyManager, self).get_query_set().filter(status=LIVE)
    
class Testimony(models.Model):
    project = models.ForeignKey(Project, related_name="testimonies")
    name = models.CharField(max_length=100,
                            help_text="The name of the person providing the testimony.")
    from_url = models.URLField(blank=True, null=True,
                               help_text="(Optional) The URL of the person providing the testimony.")
    from_company = models.CharField(max_length=100, blank=True, null=True,
                                    help_text="(Optional) The company of the person providing the testimony.")
    statement = models.TextField(help_text="The testimony. HTML allowed")
    status = models.IntegerField(choices=STATUS_CHOICES, default=NEEDS_APPROVAL)
    date_added = models.DateField(auto_now=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Testimonies'
    
    def __unicode__(self):
        return "%s... - %s (%s)" % (self.statement[:35], self.name, self.project)
    
    objects = models.Manager()
    live = TestimonyManager()
    
