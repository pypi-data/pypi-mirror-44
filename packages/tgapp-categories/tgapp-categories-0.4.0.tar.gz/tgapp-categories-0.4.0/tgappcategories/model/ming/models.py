from ming import schema as s
from ming.odm import FieldProperty, RelationProperty, ForeignIdProperty
from ming.odm.declarative import MappedClass
from ming.odm.mapper import MapperExtension
import re

from tgappcategories.model import DBSession

from depot.fields.ming import UploadedFileProperty


class UpdatePathInserting(MapperExtension):
    def before_insert(self, obj, st, sess):
        obj.path = obj.path + '.' + str(obj._id)

class Category(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'tgappcategories_categories'
        indexes = [
            ('name',),
            ('path',),
        ]
        unique_indexes = [('path',)]
        extensions = [ UpdatePathInserting ]

    _id = FieldProperty(s.ObjectId)
    
    name = FieldProperty(s.String)
    description = FieldProperty(s.String)

    images = RelationProperty('CategoryImage')

    path = FieldProperty(s.String)
    depth = FieldProperty(s.Int)

    @property
    def descendants(self):
        path = '.%s' % self._id if self.path is None else self.path
        rgx = re.compile('^%s.*' % path)
        return Category.query.find({'path': rgx, '_id': {'$ne': self._id}}).all()

    @property
    def children(self):
        next_depth = self.depth + 1
        path = '.%s' % self._id if self.path is None else self.path
        rgx = re.compile('^%s.*' % path)
        return Category.query.find({'path': rgx, 'depth': next_depth}).all()

    @property
    def parent_path(self):
        parent_path = '.'.join(self.path.split('.')[:-1])
        return parent_path if parent_path else '.'
 
    @property
    def parent(self):
        try:
            return Category.query.find({'path': self.parent_path}).first()
        except:
            return None

    @property
    def brothers(self):
        rgx = re.compile(('^%s*' % self.parent_path) if self.parent_path != '.' else '')
        return Category.query.find({'path': rgx, 'depth': self.depth, '_id': {'$ne': self._id}}).all()  

    @classmethod
    def by_path(cls, path):
        return Category.query.find({'path': path}).first()

    @classmethod
    def by_id(cls, _id):
        return Category.query.find({'_id': _id}).first()


class CategoryImage(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'tgappcategories_images'

    _id = FieldProperty(s.ObjectId)

    content = UploadedFileProperty(upload_storage='category_image')

    image_name = FieldProperty(s.String)

    category_id = ForeignIdProperty('Category')
    category = RelationProperty('Category')
