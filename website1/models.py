from django.db import models

# Create your models here. 

class Record(models.Model):
	song_type_choices = [
		('Praise', 'PRAISE'),	#making dropdown choices for song_type
		('WORSHIP', 'Worship'),
	]
	created_at = models.DateTimeField(auto_now_add=True) # sets to current date and time when the record is first created
	song_title = models.CharField(max_length=150)
	artist_name = models.CharField(max_length=100)
	song_lyrics = models.TextField()
	song_type = models.CharField(max_length=50, choices=song_type_choices)
	song_chords = models.TextField()

	def __str__(self):
		return(f"{self.song_title} {self.artist_name}")
		
