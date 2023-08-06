from homevee.VoiceAssistant.Modules.CalendarModule.add_calendar_module import VoiceAddCalendarModule
from homevee.VoiceAssistant.Modules.CalendarModule.get_calendar_module import VoiceGetCalendarModule
from homevee.VoiceAssistant.Modules.DeviceControlModule.get_sensor_data_module import VoiceDeviceGetSensorDataModule
from homevee.VoiceAssistant.Modules.DeviceControlModule.rgb_control_module import VoiceRgbDeviceControlModule
from homevee.VoiceAssistant.Modules.DeviceControlModule.set_modes_module import VoiceDeviceSetModesModule
from homevee.VoiceAssistant.Modules.ShoppingListModule.add_to_shopping_list_module import \
    VoiceAddToShoppingListModule
from homevee.VoiceAssistant.Modules.ShoppingListModule.get_shopping_list_module import VoiceGetShoppingListModule
from homevee.VoiceAssistant.Modules.add_nutrition_data_module import VoiceAddNutritionDataModule
from homevee.VoiceAssistant.Modules.calculator_module import VoiceCalculatorModule
from homevee.VoiceAssistant.Modules.conversation_module import VoiceConversationModule
from homevee.VoiceAssistant.Modules.get_activities_module import VoiceGetActivitiesModule
from homevee.VoiceAssistant.Modules.get_jokes_module import VoiceGetJokesModule
from homevee.VoiceAssistant.Modules.get_nutrition_diary_module import VoiceGetNutritionDiaryModule
from homevee.VoiceAssistant.Modules.get_nutrition_info_module import VoiceGetNutritionInfoModule
from homevee.VoiceAssistant.Modules.get_recipes_module import VoiceGetRecipesModule
from homevee.VoiceAssistant.Modules.get_summary_module import VoiceGetSummaryModule
from homevee.VoiceAssistant.Modules.get_tv_schedule_module import VoiceGetTvScheduleModule
from homevee.VoiceAssistant.Modules.get_tv_tipps_module import VoiceGetTvTippsModule
from homevee.VoiceAssistant.Modules.get_weather_module import VoiceGetWeatherModule
from homevee.VoiceAssistant.Modules.get_weekday_module import VoiceGetWeekdayModule
from homevee.VoiceAssistant.Modules.get_wikipedia_definition import VoiceGetWikipediaDefinitionModule
from homevee.VoiceAssistant.Modules.movie_api_module import VoiceMovieApiModule
from homevee.VoiceAssistant.Modules.places_api_module import VoicePlacesApiModule


def get_voice_modules():
    voice_modules = [
        VoiceAddCalendarModule(priority=1),
        VoiceGetCalendarModule(priority=1),
        VoiceAddNutritionDataModule(priority=1),
        VoiceGetActivitiesModule(priority=1),
        VoiceGetNutritionInfoModule(priority=1),
        VoiceGetRecipesModule(priority=1),
        VoiceDeviceGetSensorDataModule(priority=1),
        VoiceGetSummaryModule(priority=1),
        VoiceGetTvScheduleModule(priority=1),
        VoiceGetTvTippsModule(priority=1),
        VoiceGetWeatherModule(priority=1),
        VoiceGetWeekdayModule(priority=1),
        VoiceGetWikipediaDefinitionModule(priority=1),
        VoiceGetJokesModule(priority=1),
        VoiceMovieApiModule(priority=1),
        VoiceGetNutritionDiaryModule(priority=1),
        VoicePlacesApiModule(priority=1),
        VoiceRgbDeviceControlModule(priority=1),
        VoiceDeviceSetModesModule(priority=1),
        VoiceAddToShoppingListModule(priority=1),
        VoiceGetShoppingListModule(priority=1),
        VoiceCalculatorModule(priority=1),
        VoiceConversationModule(priority=0),
        #VoiceModule(priority=1),
    ]

    #voice_modules = sorted(voice_modules, key=lambda x: x.get_priority(), reverse=True)

    return voice_modules