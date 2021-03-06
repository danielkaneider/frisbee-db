from datetime import date
from random import choices

from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import models as authModels

# Create your models here.

class Person(models.Model):
    SEX= (
        'male',
        'female',
    )
    """ personal information"""
    firstname =models.CharField(max_length=200)
    lastname =models.CharField(max_length=200)
    birthdate = models.DateField()
    sex = models.CharField(max_length=5,choices=SEX)

    """  contact information"""
    email = models.EmailField()
    zip = models.PositiveIntegerField(max_length=10)


""" An organization is an abstract concept for people or parties
    who organize themselves for a specific purpose.  Teams, clubs
    and associations are the 3 different organization types in this model"""
class Organiation(models.Model):
    name = models.CharField(max_length='300')
    founded_on = models.DateField()
    disolved_on = models.DateField() #TODO: proper english
    description = models.TextField()
    

"""A Team is an organization owned by a Club. it consists of a list
   of players which is antemporary assignment of a player to a team"""
class Team(models.Model):


class Club(models.Model):


class Association(models.Model):

"""A player is a role of aperson in context of the sport.
   it holds"""
class Player(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(max_length=5)

""" A membership connects an organization with another organozation
    or peraon. It is reported by, and  confirmed by a person 
    it my have a from and until date. missing values asumen an infinite Membership period"""
class Membership(models.Model):
    valid_until = models.DateField()
    valid_from = models.DateField()
    reported_by: User = models.ForeignKey(authModels.User)
    approved_by: User  = models.ForeignKey(authModels.User)

    class Meta:
        abstract = True

    def is_active(self) -> bool:
        return self.valid_from <= date.now() <= self.valid_until


class PlayerToTeamMembership(Membership):
    player = models.ForeignKey(Person,on_delete=models.CASCADE)
    team = models.ForeignKey(Team,on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'PlayerToTeamMembership'

"""p """
class TeamToClubTeamMembership(Membership):
    team = models.ForeignKey(Team,on_delete=models.CASCADE)
    club = models.ForeignKey(Club,on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'TeamToClubTeamMembership'

class ClubToAssociationMembership(Membership):
    team = models.ForeignKey(Club,on_delete=models.CASCADE)
    association = models.ForeignKey(Association,on_delete=models.CASCADE)

    class Meta(Membership.Meta):
        db_table = 'ClubToAssociationMembership'

class PersonToAssociationMembership(Membership):
    ASSOCIATION_ROLES =    (
        'President',
        'Vice president',
        'Treasurer',
        'Schrifti', #TODO: change to english
        'ordinary Member'
    )
    person = models.ForeignKey(Person,on_delete=models.CASCADE)
    association = models.ForeignKey(Association,on_delete=models.CASCADE)
    role = models.CharField(choices=ASSOCIATION_ROLES)

    class Meta(Membership.Meta):
        db_table = 'PersonToAssociationMembership'