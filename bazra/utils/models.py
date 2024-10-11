from utils.mixins.base_model_mixin import BaseModelMixin

""" def user_directory_path(instance, filename):
    def genCleanUUID():
        return "".join(str(uuid.uuid4()).split("-"))

    extension = filename.split(".")[-1]
    today = timezone.now()
    path = "{}/{}/{}/{}.{}".format(today.year, f"{today.month:02}", f"{today.day:02}", genCleanUUID(), extension)
    return (instance.scope + "/" + path) if hasattr(instance, "scope") and instance.scope else path
 """


class Image(BaseModelMixin):

    class Meta:
        abstract = True
