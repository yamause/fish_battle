import logging

from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core import utils as ask_utils
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr = handler_input.attributes_manager.persistent_attributes

        if attr :
            life = attr["life"]
            max_life = attr["max_life"]
            condition_seed =  life / max_life
            
            if condition_seed == 1:
                fish_condition = "元気いっぱい"
            elif condition_seed > 0.8:
                fish_condition = "調子は普通"
            elif condition_seed > 0.5:
                fish_condition = "ちょっと疲れてる"
            else:
                fish_condition = "とても疲れてる"

            speak_output = ("こんにちは！フィッシュバトルへようこそ！あなたのフィッシュは{}みたいです。").format(fish_condition)
        else:
            attr["max_life"] = 100
            attr["life"] = 100
            attr["power"] = 100
            attr["defense"] = 100
            attr["v_count"] = 0

            handler_input.attributes_manager.persistent_attributes = attr
            handler_input.attributes_manager.save_persistent_attributes()
            speak_output = ("初めまして！フィッシュバトルへようこそ！この子があなたの新しいフィッシュです。")
            
        return (
            handler_input.response_builder
            .speak(speak_output)
            .ask(speak_output)
            .response
        )