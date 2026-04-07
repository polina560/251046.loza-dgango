from levels.models import IntroDialogue, Intro
from rest_framework import serializers

class IntroDialogueSerializer (serializers.ModelSerializer):
    class Meta:
        model = IntroDialogue
        fields = ['text', 'image']

class IntroSerializer (serializers.ModelSerializer):

    intro_dialogue = IntroDialogueSerializer(many=True, read_only=True, source='introdialogue_set')

    class Meta:
        model = Intro
        fields = ['cyclic_video', 'background_video', 'intro_dialogue']

