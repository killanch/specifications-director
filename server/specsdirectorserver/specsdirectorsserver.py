#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import ldap
from specdk.v1_0 import SDAuth
from garuda import Garuda
from garuda.channels.rest import GAFalconChannel, GAFlaskChannel
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.plugins.authentication import GASimpleAuthenticationPlugin

from plugins.logic.repositories_importer import SDRepositoryImporterLogicPlugin
from plugins.logic.repositories_exporter import SDRepositoryExporterLogicPlugin
from plugins.logic.apis import SDAPILogicPlugin
from plugins.logic.specifications import SDSpecificationLogicPlugin
from plugins.logic.attributes import SDAttributeLogicPlugin

def auth_function(request, session, root_api, storage_controller):
    """
    """
    auth = SDAuth()

    try:
        base_dn = 'uid=%s,cn=users,cn=accounts,dc=us,dc=alcatel-lucent,dc=com' % request.username
        ldap_connection = ldap.open('nuageldap1.us.alcatel-lucent.com')
        ldap_connection.bind_s(base_dn, request.token)
    except Exception as ex:
        return None

    auth.api_key = session.uuid
    auth.password = None
    auth.user_name = request.username
    return auth



def start():
    """
    """
    channel = GAFalconChannel(ssl_certificate='ssl/server.crt', ssl_key='ssl/server.key')
    storage_plugin = GAMongoStoragePlugin(db_name='specsdirector')
    authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
    sdk_infos = [{'identifier': 'default', 'module': 'specdk.v1_0'}]
    repo_import_logic_plugin = SDRepositoryImporterLogicPlugin()
    repo_export_logic_plugin = SDRepositoryExporterLogicPlugin()
    apis_logic_plugin = SDAPILogicPlugin()
    spec_logic_plugin = SDSpecificationLogicPlugin()
    attr_logic_plugin = SDAttributeLogicPlugin()

    plugins = [storage_plugin, authentication_plugin, repo_import_logic_plugin, repo_export_logic_plugin, apis_logic_plugin, spec_logic_plugin, attr_logic_plugin]

    garuda = Garuda(sdks_info=sdk_infos, channels=[channel], plugins=plugins, log_level=logging.DEBUG)
    garuda.start()


if __name__ == '__main__':
    start()

