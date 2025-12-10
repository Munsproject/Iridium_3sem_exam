import math
import random

class Narvik:
    """
    Simulerer en nødenhed i Narvik-fjeldene.

    - Før power_on(): position er statisk (enheden er slukket).
    - Efter power_on(): hver get_position() giver et nyt "skridt".
    - Efter stop_movement() (fx ved SOS): position fryser og ændrer sig ikke mere.
    """

    def __init__(self, start_lat=68.4380, start_lon=17.4273):
        # Startpunkt: Narvik-fjeldene
        self.lat = start_lat
        self.lon = start_lon

        self.is_on = False     # enhed tændt?
        self.frozen = False    # bevægelse stoppet (fx efter SOS)?

    def power_on(self):
        """Tænd enheden."""
        self.is_on = True

    def stop_moving(self):
        """
        Stop bevægelse (bruges typisk ved SOS).
        GPS'en kan stadig læses, men positionen ændrer sig ikke længere.
        """
        self.frozen = True

    def _meters_to_degree(self, dx_m, dy_m):
        """
        Konverter små bevægelser i meter til grader.
        dx_m: øst/vest (meter)
        dy_m: nord/syd (meter)
        """
        dlat = dy_m / 111_111  # meter pr. breddegrad
        dlon = dx_m / (111_111 * math.cos(math.radians(self.lat)))
        return dlat, dlon

    def _human_step(self):
        """
        Lav ét 'menneskeligt skridt' i tilfældig retning.
        """
        # Ét skridt mellem ca. 0.5 og 1.5 meter
        step_m = random.uniform(0.5, 1.5)

        # Tilfældig retning (0-360 grader)
        direction_deg = random.uniform(0, 360)

        # Bevægelse i meter (øst/vest, nord/syd)
        dx = step_m * math.cos(math.radians(direction_deg))  # øst/vest
        dy = step_m * math.sin(math.radians(direction_deg))  # nord/syd

        dlat, dlon = self._meters_to_deg(dx, dy)

        self.lat += dlat
        self.lon += dlon

    def get_position(self):
        """
        Returner GPS-position.

        - Hvis enheden ikke er tændt (is_on=False): ingen bevægelse.
        - Hvis enheden er tændt og ikke frossen: tag ét skridt før vi returnerer.
        - Hvis den er frossen: returner samme koordinat hver gang.
        """
        if self.is_on and not self.frozen:
            self._step()

        return self.lat, self.lon

