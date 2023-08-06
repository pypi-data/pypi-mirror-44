# from unittest import mock
#
# import pytest
#
# from atlas.modules.helpers.open_api import ElementConfig, Schema, constants
#
#
# class TestElementConfig:
#
#     @mock.patch('atlas.modules.helpers.open_api.ElementConfig.resolve_config')
#     def test_ref(self, patched_config):
#         patched_config.return_value = {constants.REF: "ref"}
#         instance = ElementConfig({})
#
#         assert instance.ref == "ref"
#
#     def test_resolve_config_non_array(self):
#         instance = ElementConfig({constants.TYPE: constants.OBJECT, "x": "a"})
#         assert instance.resolved_config == {constants.TYPE: constants.OBJECT, "x": "a"}
#
#     def test_resolve_config_array(self):
#         instance = ElementConfig({constants.ARRAY: constants.OBJECT, "x": "a", constants.ITEMS: {"z": "y"}})
#         assert instance.resolved_config == {"z": "y"}
#
#
# class TestSchema:
#
#     @pytest.fixture(scope='class')
#     def instance(self):
#         return Schema({})
#
#     def test_get_all_refs(self, instance):
#         instance.config = {}
#         assert instance.get_all_refs() == []
#
#     def test_with_element_ref(self, instance):
#         instance.config = {constants.REF: "ref"}
#         assert instance.get_all_refs() == ["ref"]
#
#     def test_with_array(self, instance):
#         instance.config = {
#             constants.TYPE: constants.ARRAY,
#             constants.ITEMS: {
#
#             }
#         }
