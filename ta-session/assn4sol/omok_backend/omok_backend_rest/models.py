from django.db import models

class Room(models.Model):
    player1 = models.ForeignKey('auth.User', null=True, related_name='room_as_player1', on_delete=models.CASCADE)
    player2 = models.ForeignKey('auth.User', null=True, related_name='room_as_player2', on_delete=models.CASCADE)

class History(models.Model):
    player = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='history', on_delete=models.CASCADE)
    place_i = models.IntegerField()
    place_j = models.IntegerField()
