from peewee import *

connection = {
    'user': 'py4seo',
    'password': 'PY1111forSEO',
    'host': '88.198.172.182',
    'port': 5432
}

db = PostgresqlDatabase('library', **connection)


class Category(Model):
    name = CharField(max_length=200, null=True)

    class Meta:
        database = db
        table_name = "Romanchenko_category"


class Announcement(Model):
    title = CharField(max_length=500)
    photo = CharField(max_length=500, null=True)
    link = CharField(max_length=300)
    city = CharField(max_length=150)
    category = ForeignKeyField(Category, related_name='Announcement')

    class Meta:
        database = db
        table_name = 'Romanchenko_Olga'


if __name__ == '__main__':
    db.drop_tables([Announcement, Category])
    db.create_tables([Announcement, Category])


