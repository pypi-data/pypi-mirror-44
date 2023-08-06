from ming import schema as s
from ming.odm import FieldProperty, RelationProperty, ForeignIdProperty
from ming.odm.declarative import MappedClass
from bson import ObjectId
import re

from tgappcategories.model import DBSession

from depot.fields.ming import UploadedFileProperty


class Category(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'tgappcategories_categories'
        indexes = [
            ('name',),
            ('path',),
        ]

    _id = FieldProperty(s.ObjectId)
    
    name = FieldProperty(s.String)
    description = FieldProperty(s.String)

    images = RelationProperty('CategoryImage')

    path = FieldProperty(s.String)
    depth = FieldProperty(s.Int)

    @property
    def descendants(self):
        path = '~%s' % self._id if not self.path else self.path
        rgx = re.compile('^%s~*' % path)
        return Category.query.find({'path': rgx, '_id': {'$ne': self._id}}).all()

    @property
    def children(self):
        next_depth = self.depth + 1
        path = '~%s' % self._id if self.path is None else self.path
        rgx = re.compile('^%s~*' % path)
        return Category.query.find({'path': rgx, 'depth': next_depth}).all()

    @property
    def parent(self):
        try:
            return Category.query.find({'_id': ObjectId(self.path.split('~')[-1])}).first()
        except:
            return None

    @property
    def siblings(self):
        return Category.query.find({'path': self.path, '_id': {'$ne': self._id}}).all()  


class CategoryImage(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'tgappcategories_images'

    _id = FieldProperty(s.ObjectId)

    content = UploadedFileProperty(upload_storage='category_image')

    image_name = FieldProperty(s.String)

    category_id = ForeignIdProperty('Category')
    category = RelationProperty('Category')
