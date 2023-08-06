"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from cortex.agent import Agent


class AgentBuilder:

    """
    Creates a Cortex Agent.
    """

    def __init__(self, name: str, client: CatalogClient, camel='1.0.0'):
        self._camel = camel
        self._name = name
        self._title = None
        self._description = None
        self._client = client

    def title(self, title: str):
        """
        Sets the title property.

        :param title: the human friendly name of the Agent
        :return: the builder instance
        """
        self._title = title
        return self

    def description(self, description: str):
        """
        Sets the description property of the Skill.

        :param description: the human friendly long description of the Skill
        :return: the builder instance
        """
        self._description = description
        return self


    def to_camel(self):
        skill = {
            'camel': self._camel,
            'name': self._name,
            'title': self._title or self._name,
            'inputs': list(self._inputs.values()),
            'outputs': list(self._outputs.values())

        }


        if len(self._properties) > 0:
            skill['properties'] = list(self._properties.values())

        if len(self._datasetrefs) > 0:
            skill['datasets'] = list(self._datasetrefs.values())

        if self._description:
            skill['description'] = self._description

        return skill

    def build(self) -> Skill:
        """
        Builds an Agent using the properties configured on the builder.

        :return: the resulting resource
        """
        camel = self.to_camel()
        self._client.save(camel)

        return this.__class__.get(self._name, self._client._serviceconnector)
