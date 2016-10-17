from YAMLLoader import YAMLLoader
import logging

from core.Models.Settings import Settings
from core.Models.Stt import Stt
from core.Models.Trigger import Trigger
from core.Models.Tts import Tts

FILE_NAME = "settings.yml"

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NullSettingException(Exception):
    pass


class SettingNotFound(Exception):
    pass


class SettingLoader(object):

    def __init__(self):
        pass

    @classmethod
    def get_yaml_config(cls, file_path=None):
        if file_path is None:
            file_path = FILE_NAME
        return YAMLLoader.get_config(file_path)

    @classmethod
    def get_settings(cls, file_path=None):
        """
        Return a Settings object from settings.yml file
        :return:
        """
        settings = cls.get_yaml_config(file_path)
        default_stt_name = cls._get_default_speech_to_text(settings)
        default_tts_name = cls._get_default_text_to_speech(settings)
        default_trigger_name = cls._get_default_trigger(settings)
        stts = cls._get_stts(settings)
        ttss = cls._get_ttss(settings)
        triggers = cls._get_triggers(settings)
        random_wake_up_answers = cls._get_random_wake_up_answers(settings)
        random_wake_up_sounds = cls._get_random_wake_up_sounds(settings)

        # create a setting object
        setting_object = Settings(default_stt_name=default_stt_name,
                                  default_tts_name=default_tts_name,
                                  default_trigger_name=default_trigger_name,
                                  stts=stts,
                                  ttss=ttss,
                                  triggers=triggers,
                                  random_wake_up_answers=random_wake_up_answers,
                                  random_wake_up_sounds=random_wake_up_sounds)
        return setting_object

    @staticmethod
    def _get_default_speech_to_text(settings):

        try:
            default_speech_to_text = settings["default_speech_to_text"]
            if default_speech_to_text is None:
                raise NullSettingException("Attribute default_speech_to_text is null")
            logger.debug("Default STT: %s" % default_speech_to_text)
            return default_speech_to_text
        except KeyError:
            raise SettingNotFound("Attribute default_speech_to_text not found in settings")

    @staticmethod
    def _get_default_text_to_speech(settings):
        try:
            default_text_to_speech = settings["default_text_to_speech"]
            if default_text_to_speech is None:
                raise NullSettingException("Attribute default_text_to_speech is null")
            logger.debug("Default TTS: %s" % default_text_to_speech)
            return default_text_to_speech
        except KeyError:
            raise SettingNotFound("Attribute default_text_to_speech not found in settings")

    @staticmethod
    def _get_default_trigger(settings):
        try:
            default_trigger = settings["default_trigger"]
            if default_trigger is None:
                raise NullSettingException("Attribute default_trigger is null")
            logger.debug("Default Trigger name: %s" % default_trigger)
            return default_trigger
        except KeyError:
            raise SettingNotFound("Attribute default_trigger not found in settings")

    @classmethod
    def _get_stts(cls, settings):
        """
        Return a list of stt object
        :param settings: loaded settings file
        :return: List of Stt
        """
        try:
            speechs_to_text_list = settings["speech_to_text"]
        except KeyError:
            raise NullSettingException("speech_to_text settings not found")

        stts = list()
        for speechs_to_text_el in speechs_to_text_list:
            if isinstance(speechs_to_text_el, dict):
                # print "Neurons dict ok"
                for stt_name in speechs_to_text_el:
                    name = stt_name
                    parameters = speechs_to_text_el[name]
                    new_stt = Stt(name=name, parameters=parameters)
                    stts.append(new_stt)
            else:
                # the neuron does not have parameter
                new_stt = Stt(name=speechs_to_text_el)
                stts.append(new_stt)
        return stts

    @classmethod
    def _get_ttss(cls, settings):
        """
        Return a list of Tts object
        :param settings: loaded settings file
        :return: List of Tts
        """
        try:
            text_to_speech_list = settings["text_to_speech"]
        except KeyError:
            raise SettingNotFound("text_to_speech settings not found")

        ttss = list()
        for text_to_speech_el in text_to_speech_list:
            if isinstance(text_to_speech_el, dict):
                # print "Neurons dict ok"
                for tts_name in text_to_speech_el:
                    name = tts_name
                    parameters = text_to_speech_el[name]
                    new_tts = Tts(name=name, parameters=parameters)
                    ttss.append(new_tts)
            else:
                # the neuron does not have parameter
                new_tts = Tts(name=text_to_speech_el)
                ttss.append(new_tts)
        return ttss

    @classmethod
    def _get_triggers(cls, settings):
        """
        Return a list of Trigger object
        :param settings: loaded settings file
        :return: List of Trigger
        """
        try:
            triggers_list = settings["triggers"]
        except KeyError:
            raise SettingNotFound("text_to_speech settings not found")

        triggers = list()
        for trigger_el in triggers_list:
            if isinstance(trigger_el, dict):
                # print "Neurons dict ok"
                for tts_name in trigger_el:
                    name = tts_name
                    parameters = trigger_el[name]
                    new_tts = Trigger(name=name, parameters=parameters)
                    triggers.append(new_tts)
            else:
                # the neuron does not have parameter
                new_tts = Trigger(name=trigger_el)
                triggers.append(new_tts)
        return triggers

    @classmethod
    def _get_random_wake_up_answers(cls, settings):
        """
        return a list of string
        :param settings:
        :return:
        """
        try:
            random_wake_up_answers_list = settings["random_wake_up_answers"]
        except KeyError:
            # User does not provide this settings
            return None

        # The list cannot be empty
        if random_wake_up_answers_list is None:
            raise NullSettingException("random_wake_up_answers settings is null")

        return random_wake_up_answers_list

    @classmethod
    def _get_random_wake_up_sounds(cls, settings):
        """
        return a list of string
        :param settings:
        :return: List of string
        """
        try:
            random_wake_up_sounds_list = settings["random_wake_up_sounds"]
        except KeyError:
            # User does not provide this settings
            return None

        # The the setting is present, the list cannot be empty
        if random_wake_up_sounds_list is None:
            raise NullSettingException("random_wake_up_sounds settings is empty")

        return random_wake_up_sounds_list
