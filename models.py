from tortoise.models import Model
from tortoise import fields

# TODOアイテムモデルの定義（Tortoise ORM）
class TodoItem(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=1024)
    description = fields.CharField(max_length=1024, null=True)
    completed = fields.BooleanField(default=False)

