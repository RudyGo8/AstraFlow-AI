from .sa_orm import models


class BaseModel(models.Model):
    __abstract__ = True

    class Meta:
        ordering = ["-created_at"]
        indexes = ("is_del",)
