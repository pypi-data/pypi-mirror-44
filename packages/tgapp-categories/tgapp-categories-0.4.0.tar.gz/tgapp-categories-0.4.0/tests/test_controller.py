import os
import re

import tg
from tgext.pluggable import app_model, instance_primary_key
from .base import configure_app, create_app, flush_db_changes
from tgappcategories import model
from webtest import AppError

from tgappcategories.helpers import images_with_image_name

find_urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
HERE = os.path.dirname(__file__)


class RegistrationControllerTests(object):
    def setup(self):
        self.app = create_app(self.app_config, False)

    def test_index(self):
        resp = self.app.get('/')
        assert 'HELLO' in resp.text

    def test_tgappcategories_index(self):
        resp = self.app.get('/tgappcategories', extra_environ={'REMOTE_USER': 'manager'})

        assert '/new_category' in resp.text, resp

    def test_tgappcategories_auth(self):
        try:
            self.app.get('/tgappcategories')
        except AppError as e:
            assert '401' in str(e)

    def test_create_category(self):
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one', 'description': 'pretty description'},
            upload_files=[
                ('image_small',
                 os.path.join(HERE, '..', 'tgappcategories/public/images/star.png'))
            ],
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'))
        cat = cats[0]

        assert 'category one' == cat.name, cat.name
        assert 'pretty description' == cat.description, cat.description
        assert next(i for i in cat.images if i.image_name == 'image_small').content.url.startswith('/depot/category_images/')
        assert '.%s' % cat._id == cat.path, cat.path
        assert cat.depth == 1, cat.depth

    def test_create_subcategory(self):
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one', 'description': 'pretty description'},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'))
        cat = cats[0]
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one.one', 'description': '1.1', 'parent_id': cat._id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one.one'))
        subcat = cats[0]
        assert subcat.parent._id == cat._id
        assert subcat.path == '.%s.%s' % (subcat.parent._id, subcat._id), subcat.path
        assert subcat.depth == 2, subcat.depth

    def test_update_category(self):
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one', 'description': 'pretty description'},
            upload_files=[
                ('image_small',
                 os.path.join(HERE, '..', 'tgappcategories/public/images/star.png'))
            ],
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        # Note that images are always created but with content = None
        __, cats = model.provider.query(model.Category, filters=dict(name='category one'))
        small_id = images_with_image_name(cats[0], 'image_small')[0]._id
        big_id = images_with_image_name(cats[0], 'image_big')[0]._id
        self.app.get(
            '/tgappcategories/update_category/' + str(cats[0]._id),
            params={'name': 'edited category', 'description': 'edited description',
                    'image_small_id': small_id, 'image_big_id': big_id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='edited category'),
                                        )

        assert 'edited category' == cats[0].name, cats[0].name
        assert 'edited description' == cats[0].description, cats[0].description

    def test_move_subcategory_to_root(self):
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one', 'description': 'pretty description'},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'))
        cat = cats[0]
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one.one', 'description': '1.1', 'parent_id': cat._id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )

        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one.one'))
        moving = cats[0]
        moving.images  # force lazy loading
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one.one.one', 'description': '1.1.1', 'parent_id': moving._id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one.one.one'))
        child = cats[0]
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'))
        root = cats[0]
        assert len(root.descendants) == 2
        assert len(root.children) == 1
        small_id = images_with_image_name(moving, 'image_small')[0]._id
        big_id = images_with_image_name(moving, 'image_big')[0]._id
        self.app.post(
            '/tgappcategories/update_category/' + str(moving._id),
            params={'name': 'category two', 'description': '2',
                    'parent_id': '',
                    'image_small_id': small_id, 'image_big_id': big_id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category two'))
        moved = cats[0]
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one.one.one'))
        child = cats[0]
        assert moved.path == '.%s' % moving._id, moved.path
        assert moved.depth == 1
        assert len(moved.brothers) == 1
        assert child.path == '.%s.%s' % (moved._id, child._id), child.path
        assert child.depth == 2
        

    def test_delete_category(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        self.app.get('/tgappcategories/delete_category/' + str(cats[0]._id),
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )

        count, cats = model.provider.query(model.Category,
                                           filters=dict(name='category one'),
                                           )
        assert count == 0, cats

    def test_cannot_delete_category(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
        )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
        )
        to_be_deleted = cats[0]
        self.app.post(
            '/tgappcategories/create_category',
            params={'name': 'category one.one', 'description': '1.1', 'parent_id': to_be_deleted._id},
            extra_environ={'REMOTE_USER': 'manager'},
            status=302,
        )
        
        self.app.get('/tgappcategories/delete_category/' + str(to_be_deleted._id),
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=412,
        )
        count, cats = model.provider.query(model.Category,
                                           filters=dict(name='category one'),
        )
        assert count == 1, cats
                
        

        

    def test_new_category_form(self):
        resp = self.app.get('/tgappcategories/new_category',
                            extra_environ={'REMOTE_USER': 'manager'})

        assert 'name="name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert '/create_category' in resp.text, resp

    def test_edit_category_form_404(self):
        self.app.get('/tgappcategories/edit_category',
                     extra_environ={'REMOTE_USER': 'manager'}, status=404)

    def test_edit_category_form(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category,
                                        filters=dict(name='category one'),
                                        )

        resp = self.app.get('/tgappcategories/edit_category/' + str(cats[0]._id),
                            extra_environ={'REMOTE_USER': 'manager'}
                            )

        assert 'name="name"' in resp.text, resp
        assert 'name="description"' in resp.text, resp
        assert '/update_category' in resp.text, resp

    def test_edit_category_validator(self):
        self.app.get('/tgappcategories/create_category',
                     params={'name': 'category one', 'description': 'pretty description'},
                     extra_environ={'REMOTE_USER': 'manager'},
                     status=302,
                     )
        __, cats = model.provider.query(model.Category, filters=dict(name='category one'))

        resp = self.app.get('/tgappcategories/update_category/' + instance_primary_key(cats[0], True),
                            params={'name': '', 'description': ''},
                            extra_environ={'REMOTE_USER': 'manager'})
        assert 'id="name:error">Enter a value', resp


class TestCategoriesControllerSQLA(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('sqlalchemy')


class TestCategoriesControllerMing(RegistrationControllerTests):
    @classmethod
    def setupClass(cls):
        cls.app_config = configure_app('ming')
