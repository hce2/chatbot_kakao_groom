from flask import Flask, Blueprint
from .menu import main_menu
from .hws_detail import house_welfare, house_welfare_detail
from .hws_detail import house_welfare_detail_1, house_welfare_detail_2
from .hws_detail import house_welfare_detail_3, house_welfare_detail_4
from .lease import show_lease

application = Flask(__name__)

# ----- register -------------------------------------------------------------------------------
application.register_blueprint(house_welfare.blue_house_welfare)
application.register_blueprint(main_menu.blue_main_menu)
application.register_blueprint(house_welfare_detail.blue_house_welfare_detail)
application.register_blueprint(house_welfare_detail_1.blue_house_welfare_detail_1)
application.register_blueprint(house_welfare_detail_2.blue_house_welfare_detail_2)
application.register_blueprint(house_welfare_detail_3.blue_house_welfare_detail_3)
application.register_blueprint(house_welfare_detail_4.blue_house_welfare_detail_4)
application.register_blueprint(show_lease.show_lease)
# ----------------------------------------------------------------------------------------------