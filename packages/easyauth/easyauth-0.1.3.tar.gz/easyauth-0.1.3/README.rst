easyauth: A toolkit to set up web application with authentication and authorization functionalities based on Django
====================================================================================================================
Don't need any code for authentication and authorization checking, just use configuration to enable authorization

.. image:: https://img.shields.io/travis/qingfeng0820/easyauth/master.svg
    :target: https://travis-ci.org/qingfeng0820/easyauth


`中文README <https://github.com/qingfeng0820/easyauth/blob/master/README-CN.rst>`_

License
-------

`BSD License <LICENSE.txt>`_


Source code
-----------
`Github <https://github.com/qingfeng0820/easyauth>`_


Develop environment
-------------------
- Python 2.7
- pip
- npm (can install nodejs which contains npm)


Installation
------------

from pypi

.. code-block:: shell

    pip install easyauth



Setup your own project via easyauth
-----------------------------------

1. Create your app by below command(it will create project under current folder):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: shell

    > make_project {your_app_name}

2. Setup backend which based on Django
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1). Change configurations of the easyauth and Django based project
    - You can keep the configuration as default if you just want to trial
    - Main configurations are in {your_app_name}/settings/production.py
    - {your_app_name}/settings/local.py is used for some special configuration only need enabled in development

2). Change your User mode located in {your_app_name}/models.py
    - see below example code (don't need add serializer, view and permission classes for User model)

.. code-block:: python

    from easyauth.models import AbstractUser


    class User(AbstractUser):
        # you can define additional fields
        {Other field} = models.CharField(...)
        # You can specify the some other field to be USERNAME_FIELD.
        # USERNAME_FIELD is unique field to identity an user for login
        # Default is phone
        USERNAME_FIELD = {Other field to stand for username}

        # You can specify the USER_DEPART_FIELD field if you user model is grouped by department or company
        # For with depart field case, the permitted user can only maintain the users in the same department.
        # Default value is None for USER_DEPART_FIELD.
        USER_DEPART_FIELD = "company"
        company = models.ForeignKey(Company, related_name='users', null=True)

        # Filter properties are defined in view classed for filtering.
        # But the User model related views are defined in easyauth, you cannot create or change filter properties
        # Thus there is another way to add filter properties like below in user model
        FILTER_FIELDS = ('company__name', ...)
        SEARCH_FIELDS = (...)
        ORDERING_FIELDS = ('company__name', ...)

        # PS: You can have no implementation of this class (just add 'pass' in this class) if you just want to trial.

3). Create your own models, serializers and views
    - modify {your_app_name}/models.py to add your own models

.. code-block:: python

    class DummyModel(models.Model):
        name = models.CharField(max_length=100, unique=True)
        created_time = models.DateTimeField(auto_now_add=True)

        class Meta:
            permissions = (
                ("maintain_dummy_model", _("Can maintain dummy model")),   # <=== define a permission in your model
            )
            ordering = ('id', )

- create {your_app_name}/serializers.py to add your own serializers

.. code-block:: python

        from rest_framework import serializers

        from {your_app_name} import models

        class DummyModelSerializer(serializers.ModelSerializer):

            class Meta:
                model = models.DummyModel
                fields = '__all__'
                depth = 1


- create {your_app_name}/permissions.py to add your own permission classes

.. code-block:: python

    from easyauth.permissions import DBBasedPermissionsAll


    class DummyModelMaintainPermission(DBBasedPermissionsAll):
        required_permission_names = ["{your_app_name}.maintain_dummy_model", ]    # <=== permission check class for the defined permission in your model

- create {your_app_name}/views.py to add your own views

.. code-block:: python

    from rest_framework import viewsets, permissions

    from {your_app_name} import models, serializers
    from {your_app_name}.permissions import DummyModelMaintainPermission

    class DummyModelViewSet(viewsets.ModelViewSet):
        queryset = models.DummyModel.objects.all()
        serializer_class = serializers.DummyModelSerializer
        permission_classes = (DummyModelMaintainPermission, )                   # <=== use the defined permission class
        # Or you can the common permission class DjangoModelPermissions instead, which provided by Rest framework lib
        #  permission_classes = (permissions.DjangoModelPermissions, )

- modify {your_app_name}/urls.py to add your API urls

.. code-block:: python

    from django.conf.urls import url, include
    from rest_framework import routers

    from easyauth import urls as auth_urls
    from easyauth import admin_urls as user_admin_urls

    from {your_app_name} import views

    router = routers.DefaultRouter(trailing_slash=False)
    # app apis
    router.register(r'api/dummy_models', views.DummyModelViewSet, base_name='dummy_model') # <=== define your API url

    urlpatterns = router.urls

    urlpatterns += [
        # url(r'^admin/', admin.site.urls),
        # auth apis including login, password reset
        url(r'^api-auth/', include(auth_urls)),            # <=== authentication APIs provided by easyauth
        # user crud apis - only used by administrator
        url(r'^api/', include(user_admin_urls)),           # <=== user/group/permission admin APIs provided by easyauth
    ]

4). Go to {your_app_name} folder to initiate database
    - run below commands:

.. code-block:: shell

    {your_app_name}> python manage.py makemigrations
    {your_app_name}> python manage.py makemigrations {your_app_name}
    {your_app_name}> python manage.py migrate

5). Then create a superuser
    - run below command:

.. code-block:: shell

    {your_app_name}> python manage.py createsuperuser

6). Start your backend for your development test
    - run below command:

.. code-block:: shell

    {your_app_name}> python manage.py runserver 0.0.0.0:80

7). Have a test
    - Maintain authentication and authorization test
        - User the created super user to login
        - Create roles/groups
        - Create users, and assign them proper roles or permissions
    - All APIs provided by easyauth
        - user group(role) admin APIs (super user or have related permissions)
            - /api/groups GET: Get all user groups (super user or have 'query_group' permission)
            - /api/groups POST: Create an user group  (super user)
            - /api/groups/[group_id] GET: Get an user group  (super user or have 'query_group' permission)
            - /api/groups/[group_id] PUT or PATCH: Modify an user group (super user)
            - /api/groups/[group_id] DELETE: Delete an user group (super user)
        - user admin APIs (super user or have related permissions, if department enabled for user model, user can only maintain users in the same department if he/she has related permissions)
            - /api/users GET: Get all users (super user or have 'query_user' permission)
            - /api/users POST: Create an user (super user or have 'create_user' permission)
            - /api/users/[user_id] GET: Get a specific user (super user or have 'query_user' permission)
            - /api/users/[user_id] PUT or PATCH: Modify a specific user  (super user or have 'change_user' permission)
            - /api/users/[user_id] DELETE: Delete a specific user   (super user or have 'delete_user' permission)
            - /api/users/[user_id]/reset/password PUT: Reset to default password for a specific user (super user or have 'change_user' permission)
        - query permission APIs (permissions are defined in models code)
            - /api/permissions GET: Get all permissions (super user or have 'query_permission' permission)
            - /api/permissions/[permission_id] GET: Get a specific permission (super user or have 'query_permission' permission)
        - authentication APIs
            - /api-auth/login POST: User login
            - /api-auth/logout POST (or GET if enabled): User logout
            - /api-auth/me PUT or PATCH: Modify current login user
            - /api-auth/me GET: Get current login user
            - /api-auth/password/change PUT: Change the current login user's password
            - /api-auth/register POST: Register User (This API can be disabled by configuration)
        - Your own APIs
            - ...


3. Setup frontend if you need admin dashboard, which based Vue + Element-UI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
1). Go to {your_app_name}/vue-ui folder, and run below command to install dependency libs
    - run below command:

.. code-block:: shell

    {your_app_name}/vue-ui> npm install

2). Configure your backend baseURL by changing {your_app_name}/vue-ui/src/components/config.js
    - see below code:

.. code-block:: javascript

    var baseURL = 'http://localhost';                // <=== baseURL for production
    if (process.env.NODE_ENV == 'development') {
        baseURL = 'http://localhost';                // <=== baseURL for development
    }
    ...

3). Change theme by alias in {your_app_name}/vue-ui/build/webpack.base.conf.js
    - Change the value of alias 'THEME'
    - Now support two themes
        - resolve('src/themes/default')             // <=== default theme
        - resolve('src/themes/green')               // <=== green theme

4). Create your own vue pages to {your_app_name}/vue-ui/src/components/page/
    - Common pages are under {your_app_name}/vue-ui/src/components/common/

5). Change the menu in left slider bar by changing {your_app_name}/vue-ui/src/components/menus.js
    - see below example code:

.. code-block:: javascript

    import i18n from '../i18n/i18n'
    import permission from './common/permission'
    import Dashboard from '@/components/page/Dashboard'
    import UserAdmin from '@/components/page/UserAdmin'
    import RoleAdmin from '@/components/page/RoleAdmin'     // RoleAdmin and UserAdmin are default pages, you can just use it.
    import YourSubMenuItem from '@/components/page/YourSubMenuItem'
    import YourSubSubMenuItem from '@/components/page/YourSubSubMenuItem'

    var menu = [
            {
                name: 'Dashboard',
                path: '/dashboard',
                component: Dashboard,
                icon: 'el-icon-lx-home',
                meta: {
                    getTitle: function() {
                        return i18n.t("page.homeTitle")
                    },
                },
            },
            {
                name: 'UserAdmin',
                path: '/userAdmin',
                component: UserAdmin,
                icon: 'el-icon-lx-people',
                meta: {
                    getTitle:  function() {
                        return i18n.t("page.userAdminTitle")
                    },
                    // must have all permissions listed below to access this menu item
                    requiredPermissions: ['query_group', 'query_permission', 'add_user', 'change_user', 'delete_user'],
                },
            },
            {
                name: 'RoleAdmin',
                path: '/roleAdmin',
                component: RoleAdmin,
                icon: 'el-icon-lx-group',
                meta: {
                        getTitle: function() {
                            return i18n.t("page.roleAdminTitle")
                        },
                        permissionCheck: function(user) {
                            return permission.isSuperUser(user)
                        }
                    },
            },
            {
                name: 'YourFolderMenu',
                icon: 'xxx',
                meta: {
                        getTitle: function() {
                            return "Your Folder Menu"
                        },
                        notRequireAuth: true,                       // <=== this configuration item means this menu can access by anonymous user
                    },
                subs: [
                      {
                          name: 'YourSubFolderMenu',
                          meta: {
                              getTitle: function() {
                                 return "Your Sub Folder Menu"
                              },
                              requiredPermissions: [...],
                          },
                          subs: [
                               // only can support three levels menu
                               {
                                   name: 'YourSubSubMenuItem',
                                   path: '/yourSubSubMenuItem',
                                   component: YourSubSubMenuItem,
                                   meta: {
                                       getTitle: function() {
                                           return "Your Sub Sub Menu Item"
                                       },
                                   },
                               },
                               ...

                          ]
                      },
                      {
                          name: 'YourSubMenuItem',
                          path: '/yourSubMenuItem',
                          component: YourSubMenuItem,
                          meta: {
                               getTitle: function() {
                                   return "Your Sub Menu Item"
                               },
                               requiredPermissions: ['maintain_dummy_model', ...],    // <=== Use the defined permission in your model
                          },
                      },
                      ...
                ]
            },
    ]


- screen shot for above menu
.. image:: img/ui.JPG

6). Modify UserAdmin.vue page
    - If you have additional fields in your User model, you can change the UserAdmin.vue to support them
        - Add columns in <el-table> for additional fields
        - Add form items in <el-dialog> of editing user for additional fields
        - Change related javascript code in that page

7). Build you pages
    - run below command:

.. code-block:: shell

    {your_app_name}/vue-ui> npm run build

8). Deploy build results to static folder
    - run below commands:

.. code-block:: shell

    {your_app_name}> mkdir static
    {your_app_name}> cp vue-ui/build/* static/

9). Access you pages
    - Visit http://localhost/static/index.html

10). if you are focus on pages development, you can use use dev model instead of steps 7 - 9
    - run below command, then visit http://localhost:8080:

.. code-block:: shell

    {your_app_name}/vue-ui> npm run build


More configurations
-------------------


Language configuration
^^^^^^^^^^^^^^^^^^^^^^^^
- Change to be Chinese
    - Change LANGUAGE_CODE = 'zh-hans' in {your app name}/settings/production.py (backend)
    - Change defaultLangCode: "zh-hans" in {your_app_name}/vue-ui/src/components/config.js (frontend)

.. code-block:: javascript

    ...
    const config = {
        loginFieldName: "phone",                         // <=== should keep this value same as USERNAME_FIELD in your User model
        backendBaseURL: baseURL,
        requestTimeout: 10000,
        defaultLangCode: "zh-hans",                      // <=== Change here for frontend
    }
    ...


easyauth Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

Change EASYAUTH_CONF in {your_app_name}/settings/product.py if you need:

.. code-block:: python

    EASYAUTH_CONF = {
        'USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN': "12345678",
        'ACCOUNT_LOGOUT_ON_GET': False,
        'DISABLE_REGISTER': False,
        'LANG_PARAM': 'lang',
    }

+----------------------------------------+------------+--------------------------------------------------------------+
| Configuration Item                     | Type       | Description                                                  |
+========================================+============+==============================================================+
| USER_DEFAULT_PWD_MAINTAIN_BY_ADMIN     | string     | Define the default password for maintaining by administrator.|
|                                        |            |                                                              |
|                                        |            | Default value is 123456 for absent                           |
+----------------------------------------+------------+--------------------------------------------------------------+
| ACCOUNT_LOGOUT_ON_GET                  | bool       | Switch for enabling GET method for logout API.               |
|                                        |            |                                                              |
|                                        |            | Default value is False for absent                            |
+----------------------------------------+------------+--------------------------------------------------------------+
| DISABLE_REGISTER                       | bool       | Switch for disabling register API.                           |
|                                        |            |                                                              |
|                                        |            | Default value is False for absent                            |
+----------------------------------------+------------+--------------------------------------------------------------+
| LANG_PARAM                             | string     | Set the language parameter name in http request.             |
|                                        |            | (Usually don't need to change it)                            |
|                                        |            |                                                              |
|                                        |            | Default value is lang, it will be used like                  |
|                                        |            | http://localhost/api/users?lang=zh-hans                      |
|                                        |            |                                                              |
|                                        |            | Tips: Keep the value of lang_param in                        |
|                                        |            | {your_app_name}/vue-ui/src/components/common/easyauth.js     |
|                                        |            | same with this configuration value.                          |
+----------------------------------------+------------+--------------------------------------------------------------+

More examples please see the test app in this repo




