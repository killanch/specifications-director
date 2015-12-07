import logging

from garuda.core.models import GAError, GAPluginManifest, GARequest, GAPushEvent
from garuda.core.plugins import GALogicPlugin
from garuda.core.lib import GASDKLibrary

logger = logging.getLogger('specsdirector.plugins.logic.specifications')

class SDSpecificationLogicPlugin(GALogicPlugin):
    """

    """
    @classmethod
    def manifest(cls):
        """

        """
        return GAPluginManifest(name='specifications logic', version=1.0, identifier="specsdirector.plugins.logic.specifications",
                                subscriptions={
                                    "specification": [GARequest.ACTION_DELETE, GARequest.ACTION_CREATE, GARequest.ACTION_UPDATE]
                                })

    def did_register(self):
        """
        """
        self._old_names = {};
        self._sdk = GASDKLibrary().get_sdk('default')
        self._storage_controller = self.core_controller.storage_controller
        self._github_operations_controller = self.core_controller.additional_controller(identifier='sd.controller.githuboperations.client')

    def will_perform_write(self, context):
        """
        """

        if context.request.action in (GARequest.ACTION_DELETE):
            return context

        repository     = context.parent_object
        specification  = context.object
        action         = context.request.action

        specification.name = '%s.spec' % specification.object_rest_name

        response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, parent=repository, resource_name=self._sdk.SDSpecification.rest_name, filter='name == "%s"' % specification.name)

        if response.count and response.data[0].id != specification.id:
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Duplicate Name', description='Another specification exists with the name %s' % specification.name, property_name='name'))

        if not specification.object_rest_name or not len(specification.object_rest_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute objectRESTName is mandatory.', property_name='objectRESTName'))

        if not specification.object_resource_name or not len(specification.object_resource_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute objectResourceName is mandatory.', property_name='objectResourceName'))

        if not specification.entity_name or not len(specification.entity_name):
            context.add_error(GAError(type=GAError.TYPE_CONFLICT, title='Missing attribute', description='Attribute entityName is mandatory.', property_name='entityName'))

        if action == GARequest.ACTION_UPDATE:

            response = self._storage_controller.get(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDSpecification.rest_name, identifier=specification.id)

            if response.data and response.data.name != specification.name:
                self._old_names[context.request.uuid] = response.data.name

        response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDAPIInfo.rest_name, parent=repository)
        apiinfo = response.data[0] if response.count else None

        if specification.root:

            response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDSpecification.rest_name, parent=repository, filter='name == "%s.spec"' % apiinfo.root)
            current_root_specification = response.data[0] if response.count else None

            if current_root_specification and current_root_specification.id != specification.id:
                current_root_specification.root = False
                response = self._storage_controller.update(user_identifier=context.session.root_object.id, resource=current_root_specification)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=current_root_specification))

                response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDChildAPI.rest_name, parent=current_root_specification)

                for api in response.data:
                    api.relationship = 'child'
                    response = self.core_controller.storage_controller.get(user_identifier=context.session.root_object.id,
                                                                           resource_name=self._sdk.SDSpecification.rest_name,
                                                                           identifier=api.associated_specification_id)
                    api.path = '/%s/id/%s' % (current_root_specification.object_resource_name, response.data.object_resource_name)

                    self._storage_controller.update(user_identifier=context.session.root_object.id, resource=api)
                    context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=api))

                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=current_root_specification,
                                                                        commit_message="Updated specification %s" % current_root_specification.name,
                                                                        session_username=context.session.root_object.id)

            if apiinfo and apiinfo.root != specification.object_rest_name:
                apiinfo.root = specification.object_rest_name
                self._storage_controller.update(user_identifier=context.session.root_object.id, resource=apiinfo)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=apiinfo))
                self._github_operations_controller.commit_apiinfo(repository=repository,
                                                                   apiinfo=apiinfo,
                                                                   commit_message="Updated api.info",
                                                                   session_username=context.session.root_object.id)

            response = self._storage_controller.get_all(user_identifier=context.session.root_object.id, resource_name=self._sdk.SDChildAPI.rest_name, parent=specification)

            for api in response.data:
                api.relationship = 'root'
                api.path = '/%s' % api.path.split('/')[3]
                self._storage_controller.update(user_identifier=context.session.root_object.id, resource=api)
                context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=api))

        return context

    def did_perform_write(self, context):
        """
        """
        action        = context.request.action
        specification = context.object
        repository    = context.parent_object
        session_username = context.session.root_object.id

        if action == GARequest.ACTION_CREATE:

            self._github_operations_controller.commit_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Added specification %s" % specification.name,
                                                                    session_username=session_username)

        elif action == GARequest.ACTION_UPDATE:

            if context.request.uuid in self._old_names:
                old_name = self._old_names[context.request.uuid]
                del self._old_names[context.request.uuid]

                apis = self._get_all_related_child_api(context=context)

                for api in apis:
                    components = api.path.split('/')
                    components[-1] = specification.object_resource_name
                    api.path = "/".join(components)
                    self._storage_controller.update(user_identifier=context.session.root_object.id, resource=api)
                    context.add_event(GAPushEvent(action=GARequest.ACTION_UPDATE, entity=api))

                self._github_operations_controller.rename_specification(repository=repository,
                                                                        specification=specification,
                                                                        old_name=old_name,
                                                                        commit_message="Renamed specification from %s to %s" % (old_name, specification.name),
                                                                        session_username=session_username)
            else:
                self._github_operations_controller.commit_specification(repository=repository,
                                                                        specification=specification,
                                                                        commit_message="Updated specification %s" % specification.name,
                                                                        session_username=session_username)


        elif action == GARequest.ACTION_DELETE:

            apis = self._get_all_related_child_api(context=context)

            if len(apis):
                self._storage_controller.delete_multiple(user_identifier=context.session.root_object.id, resources=apis)
                context.add_events([GAPushEvent(action=GARequest.ACTION_DELETE, entity=api) for api in apis])

            self._github_operations_controller.delete_specification(repository=repository,
                                                                    specification=specification,
                                                                    commit_message="Deleted specification %s" % specification.name,
                                                                    session_username=session_username)
        return context

    # Utilities

    def _get_all_related_child_api(self, context):
        """
        """
        apis = []

        response = self._storage_controller.get_all(user_identifier=context.session.root_object.id,
                                                    parent=context.parent_object,
                                                    resource_name=self._sdk.SDSpecification.rest_name)

        for spec in response.data:

            response = self._storage_controller.get_all(user_identifier=context.session.root_object.id,
                                                        parent=spec,
                                                        resource_name=self._sdk.SDChildAPI.rest_name,
                                                        filter='associatedSpecificationID == "%s"' % context.object.id)
            if response.count:
                apis += response.data

        return apis
