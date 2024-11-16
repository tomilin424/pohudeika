from .registration import register_registration_handlers
from .nutrition import register_nutrition_handlers
from .workout import register_workout_handlers
from .subscription import register_subscription_handlers

def register_all_handlers(dp):
    register_registration_handlers(dp)
    register_nutrition_handlers(dp)
    register_workout_handlers(dp)
    register_subscription_handlers(dp) 