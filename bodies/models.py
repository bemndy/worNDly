from django.db import models

# Create your models here.

class CelestialBody(models.Model):
    # fields
    region = models.ForeignKey('Region', on_delete=models.CASCADE)
    body_type = models.CharField(max_length=50)
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=200)

    # body info
    description = models.TextField()
    gravity = models.FloatField()   
    mass =  models.FloatField()
    radius = models.FloatField()

    # methods
    def __str__(self):
        return self.name
    
class Region(models.Model):
    # fields
    galaxy = models.CharField(max_length=100)
    solar_system = models.CharField(max_length=100)
    
    # methods
    def __str__(self):
        return self.galaxy
    
class Environment(models.Model):
    # fields
    celestial_body = models.ForeignKey('CelestialBody', on_delete=models.CASCADE)
    surface_temperature = models.FloatField()
    atmospheric_composition = models.TextField()
    weather_conditions = models.TextField()
    surface_pressure = models.FloatField()
    magnetic_field_strength = models.FloatField()

    # methods
    def __str__(self):
        return f"Environment of {self.celestial_body.name}"

class Limitations(models.Model):
    '''Model to represent the limitations, in terms of engineering equipment/technology that can 
       be provided in each satellite, rover, shuttle, etc. to explore the celestial body.
    '''
    # fields
    celestial_body = models.ForeignKey('CelestialBody', on_delete=models.CASCADE)
    enviorment = models.ForeignKey('Environment', on_delete=models.CASCADE)

    # graphical like scale for website
    exploration_difficulty = models.CharField(max_length=100)
    human_survivability = models.CharField(max_length=100)

    # use weather_condtiions, surface_pressure, surface_temperature, atmospheric_composition and weather_conditions to determine the surface mobility
    surface_mobility = models.CharField(max_length=100)

    # numerical values for backend calculations using methods below
    fuel_contraints = models.FloatField()
    data_communication_delay = models.FloatField()
    distance_from_earth = models.FloatField()

    power_requirements = models.FloatField()
    distance_from_sun = models.FloatField()

    # use magnetic_field_strength and radiation_levels to determine the radiation protection requirements
    radiation_protection = models.CharField(max_length=100)
    radiation_levels = models.FloatField()

    # methods
    def __str__(self):
        return f"Limitations of {self.celestial_body.name}"
    
    def calculate_exploration_difficulty(self):
        '''Calculate the exploration difficulty based on the various factors. This is a placeholder function and can be expanded with actual logic.'''
        difficulty_score = (self.fuel_contraints + self.data_communication_delay + self.distance_from_earth) / 3
        if difficulty_score < 5:
            return "Low"
        elif difficulty_score < 10:
            return "Medium"
        else:
            return "High"
        
    def calculate_human_survivability(self):
        '''Calculate the human survivability based on the various factors. This is a placeholder function and can be expanded with actual logic.'''
        survivability_score = (self.radiation_levels + self.surface_pressure) / 2
        if survivability_score < 5:
            return "High"
        elif survivability_score < 10:
            return "Medium"
        else:
            return "Low"
        
    def calculate_surface_mobility(self):
        '''Calculate the surface mobility based on the various factors. This is a placeholder function and can be expanded with actual logic.'''
        mobility_score = (self.distance_from_sun + self.surface_temperature) / 2
        if mobility_score < 5:
            return "High"
        elif mobility_score < 10:
            return "Medium"
        else:
            return "Low"
        
    def fuel_constraints_analysis(self):
        '''Analyze the fuel constraints based on the distance from Earth and the celestial body's gravity. This is a placeholder function and can be expanded with actual logic.'''
        if self.distance_from_earth < 100:
            return "Low"
        elif self.distance_from_earth < 1000:
            return "Medium"
        else:
            return "High"
        
    def communication_delay_analysis(self):
        '''Analyze the communication delay based on the distance from Earth. This is a placeholder function and can be expanded with actual logic.'''
        if self.data_communication_delay < 1:
            return "Low"
        elif self.data_communication_delay < 10:
            return "Medium"
        else:
            return "High"
        
    def radiation_protection_analysis(self):
        '''Analyze the radiation protection requirements based on the radiation levels. This is a placeholder function and can be expanded with actual logic.'''
        if self.radiation_levels < 5:
            return "Low"
        elif self.radiation_levels < 10:
            return "Medium"
        else:
            return "High"