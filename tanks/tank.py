from role import Role
from structural import Structural
from qualitie import Qualitie
from performance import Performance
from armament import Armament
class Tank:
    def __init__(self,type,name,country,userCountries,manufacturer,serviceYear,status,crew,roles,qualities,structural,performance,armament,variants):
        self.type = type
        self.name = name
        self.Country = country
        self.userCountries = userCountries
        self.Manufacturer = manufacturer
        self.serviceYear = serviceYear
        self.status = status
        self.crew = crew
        self.variants = variants
        if not isinstance(structural, Structural):
            raise TypeError("The parameter \"structural\" must be a instance of the \"Structural\"'s classe")
        self.structural = structural
        if not all(isinstance(roles, Role) for roletank in roles) :
            raise TypeError("The parameter \"roles\" must be a instance of the \"Role\"'s classe")
        self.roles = roles
        if not all(isinstance(qualities, Qualitie) for qualitiestank in qualities):
            raise TypeError("The parameter \"qualities\" must be a instance of the \"Qualitie\"'s classe")
        self.qualities = qualities
        if not isinstance(performance, Performance):
            raise TypeError("The parameter \"performance\" must be a instance of the \"Performance\"'s classe")
        self.performance = performance
        if not isinstance(armament, Armament):
            raise TypeError("The parameter \"armament\" must be a instance of the \"Armament\"'s classe")
        self.armament = armament


