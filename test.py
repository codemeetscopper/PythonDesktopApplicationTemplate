from common.configuration.parser import ConfigurationManager
from common.configuration.models import PageMappingEntry


config = ConfigurationManager("config/configuration.json")
print(config.user_settings["sample_text_input"].value)

# config.user_settings["sample_text_input"].value = "New Value"
# config.save_user_settings()

# new_entry = PageMappingEntry(
#     widget_ref="frontend.core.pages.new.new_c",
#     enabled=True,
#     index=7,
#     icon="images/new.svg",
#     selectable=True,
#     license_required=False
# )

# config.add_page_mapping("defaults", "NewPage", new_entry)