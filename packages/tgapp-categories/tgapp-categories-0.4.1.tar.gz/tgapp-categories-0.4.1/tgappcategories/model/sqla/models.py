from sqlalchemy import Column, ForeignKey, event
from sqlalchemy.types import Unicode, Integer

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound

from depot.fields.sqlalchemy import UploadedFileField
from tgext.pluggable import app_model


DeclarativeBase = declarative_base()


class Category(DeclarativeBase):
    __tablename__ = 'tgappcategories_categories'

    _id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(Unicode(255))
    description = Column(Unicode(1024))

    path = Column(Unicode(255), nullable=True)
    depth = Column(Integer)

    @property
    def descendants(self):
        path = '~%s' % self._id if self.path is None else self.path
        return app_model.DBSession.query(Category).filter(Category.path.like(path + '~%')).all()

    @property
    def children(self):
        try:
            next_depth = self.depth + 1
        except AttributeError:  # pragma: no cover
            # when self.depth is None, for migrated categories before version 0.4.0
            next_depth = 1
        return app_model.DBSession.query(Category).filter(Category.path.like(self.path + '~%'), Category.depth == next_depth).all()

    @property
    def parent(self):
        try:
            return app_model.DBSession.query(Category).filter(Category._id == self.path.split('~')[-1]).one()
        except NoResultFound:
            return None

    @property
    def siblings(self):
        return app_model.DBSession.query(Category).filter(Category.path == self.path, Category._id != self._id).all()

    @classmethod
    def by_id(cls, _id):
        return app_model.DBSession.query(cls).filter(cls._id == _id).one()


class CategoryImage(DeclarativeBase):
    __tablename__ = 'tgappcategories_images'

    _id = Column(Integer, autoincrement=True, primary_key=True)

    content = Column(UploadedFileField(upload_storage='category_image'))

    image_name = Column(Unicode(255))

    category_id = Column(Integer, ForeignKey('tgappcategories_categories._id'))
    category = relationship('Category', backref='images')
