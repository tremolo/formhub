from test_base import MainTestCase
from main.models import UserProfile
from main.views import edit
from django.core.urlresolvers import reverse
from odk_logger.models import XForm
from main.models import MetaData
from main.views import set_role, show
from odk_logger.views import delete_xform

class TestPeopleRoles(MainTestCase):

    def setUp(self):
        MainTestCase.setUp(self)
        self.set_role_url = reverse(set_role)
        self._create_user_and_login()
        self._publish_transportation_form()
        self.form_show_url = reverse(show, kwargs={
            'username': self.user.username,
            'id_string': self.xform.id_string
        })
        UserProfile.objects.get_or_create(user=self.user)

    def test_admin_can_change_role(self):
        user = self._create_user('alice', 'alice')
        UserProfile.objects.get_or_create(user=user)
        self.user.profile.role = 10
        self.user.profile.save()
        response = self.client.post(self.set_role_url, {'role': 10, 'username': user.username},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)

    def test_viewer_cant_change_role(self):
        user = self._create_user('alice', 'alice')
        response = self.client.post(self.set_role_url, {'role': 10, 'username': user.username},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 403)

    def test_admin_can_see_edit(self):
        self.user.profile.role = 10
        self.user.profile.save()
        response = self.client.get(self.form_show_url)
        self.assertContains(response, 'edit</a>')

    def test_viewer_cant_see_edit(self):
        response = self.client.get(self.form_show_url)
        self.assertNotContains(response, 'edit</a>')

