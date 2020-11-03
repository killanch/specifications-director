#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import logging
#import simpleldap
import os
import specdk.v1_0 as specdk

from garuda import Garuda
from garuda.channels.rest import GAFalconChannel
from garuda.plugins.storage import GAMongoStoragePlugin
from garuda.plugins.authentication import GASimpleAuthenticationPlugin
from garuda.plugins.permissions import GAOwnerPermissionsPlugin

from plugins.logic.abstracts import SDAbstractLogicPlugin
from plugins.logic.apiinfo import SDAPIInfoLogicPlugin
from plugins.logic.apis import SDAPILogicPlugin
from plugins.logic.attributes import SDAttributeLogicPlugin
from plugins.logic.jobs import SDJobLogicPlugin
from plugins.logic.monolitheconfig import SDMonolitheConfigLogicPlugin
from plugins.logic.repositories import SDRepositoryLogicPlugin
from plugins.logic.specifications import SDSpecificationLogicPlugin
from plugins.logic.tokens import SDTokenLogicPlugin

from lib import SDGitHubOperationsController, SDGitHubOperationsClient

logger = logging.getLogger('specsdirector')


def auth_function(request, session, root_object_class, storage_controller):
    """
    """
    auth = root_object_class()

    if 'NO_AUTHENTICATION' not in os.environ:

        base_dn = os.environ['LDAP_BASE_DN_TEMPLATE'] % request.username  # 'uid=%s,cn=users,cn=accounts,dc=us,dc=alcatel-lucent,dc=com' % request.username
        ldap_connection = simpleldap.Connection(os.environ['LDAP_ADDRESS'])  # 'nuageldap1.us.alcatel-lucent.com'

        if not ldap_connection.authenticate(base_dn, request.token):
            return None

    auth.id = request.username
    auth.api_key = session.uuid
    auth.password = None
    auth.user_name = request.username
    return auth


def db_init(db, root_object_class):
    """
    """
    import pymongo
    db[specdk.SDJob.rest_name].create_index('lastUpdatedDate', expireAfterSeconds=600)
    db[specdk.SDSpecification.rest_name].create_index([('name', pymongo.TEXT)])


def start(falcon_port, mongo_host, mongo_port, mongo_db, redis_host, redis_port, redis_db):
    """
    """
    # redis
    redis_info = {'host': redis_host, 'port': redis_port, 'db': redis_db}

    # mongo
    mongo_uri = 'mongodb://%s:%d' % (mongo_host, mongo_port)

    if os.path.exists("/certificates"):
        channel = GAFalconChannel(port=falcon_port, ssl_certificate='/certificates/server.pem', ssl_key='/certificates/server.key')
    else:
        channel = GAFalconChannel(port=falcon_port)

    storage_plugin = GAMongoStoragePlugin(db_name=mongo_db, mongo_uri=mongo_uri, db_initialization_function=db_init)
    authentication_plugin = GASimpleAuthenticationPlugin(auth_function=auth_function)
    permissions_plugin = GAOwnerPermissionsPlugin()
    sdk_infos = [{'identifier': 'default', 'module': 'specdk.v1_0'}]

    plugins = [storage_plugin,
               authentication_plugin,
               permissions_plugin,
               SDJobLogicPlugin(),
               SDAPILogicPlugin(),
               SDSpecificationLogicPlugin(),
               SDAbstractLogicPlugin(),
               SDAttributeLogicPlugin(),
               SDAPIInfoLogicPlugin(),
               SDRepositoryLogicPlugin(),
               SDMonolitheConfigLogicPlugin(),
               SDTokenLogicPlugin()]

    garuda = Garuda(sdks_info=sdk_infos,
                    redis_info=redis_info,
                    channels=[channel],
                    additional_controller_classes=[SDGitHubOperationsClient],
                    additional_master_controller_classes=[SDGitHubOperationsController],
                    plugins=plugins,
                    log_level=logging.DEBUG)

    logger.info('starting specification director')
    garuda.start()


if __name__ == '__main__':

    garuda_port = int(os.environ['GARUDA_PORT']) if 'GARUDA_PORT' in os.environ else 1984
    garuda_mongo_host = os.environ['GARUDA_MONGO_HOST'] if 'GARUDA_MONGO_HOST' in os.environ else '127.0.0.1'
    garuda_mongo_port = int(os.environ['GARUDA_MONGO_PORT']) if 'GARUDA_MONGO_PORT' in os.environ else 27017
    garuda_mongo_db = os.environ['GARUDA_MONGO_DB'] if 'GARUDA_MONGO_DB' in os.environ else 'specsdirector'
    garuda_redis_host = os.environ['GARUDA_REDIS_HOST'] if 'GARUDA_REDIS_HOST' in os.environ else '127.0.0.1'
    garuda_redis_port = int(os.environ['GARUDA_REDIS_PORT']) if 'GARUDA_REDIS_PORT' in os.environ else 6379
    garuda_redis_db = int(os.environ['GARUDA_REDIS_DB']) if 'GARUDA_REDIS_DB' in os.environ else 6

    start(falcon_port=garuda_port,
          mongo_host=garuda_mongo_host,
          mongo_port=garuda_mongo_port,
          mongo_db=garuda_mongo_db,
          redis_host=garuda_redis_host,
          redis_port=garuda_redis_port,
          redis_db=garuda_redis_db)
