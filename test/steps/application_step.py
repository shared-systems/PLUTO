from src.app import App
from mainapp import MainApp

from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt, pyqtSignal

from behave import use_step_matcher, given, when, then, step

from steps.helpers_step import assert_equal, assert_is_not
use_step_matcher("re")


@when(r'I open the application window')
def open_application(context):
    context.app = context.__app.app
    assert_is_not(context.app, None)


@when(r'I click on the (dashboard|resources|jobs) tab')
def open_main_tab(context, tab):
    if tab == "dashboard":
        QTest.mouseClick(context.app.sidebar.dashboard, Qt.LeftButton)
    elif tab == "resources":
        QTest.mouseClick(context.app.sidebar.resources, Qt.LeftButton)
    elif tab == "jobs":
        QTest.mouseClick(context.app.sidebar.jobs, Qt.LeftButton)


@then(r'the current tab should be the (dashboard|resources|jobs) tab')
def verify_main_tab(context, tab):
    from dashboard import Dashboard
    from resources import Resources
    from jobs import Jobs

    check_type = lambda type_: assert_equal(type(context.app.main_window.stack.currentWidget()), type_)

    if tab == "dashboard":
        check_type(Dashboard)
    elif tab == "resources":
        check_type(Resources)
    elif tab == "jobs":
        check_type(Jobs)


@when(r'I logout of the application')
def logout_of_application(context):
    QTest.mouseClick(context.app.navigation.menu_button, Qt.LeftButton)
    QTest.mouseClick(context.app.account.logout, Qt.LeftButton)


@then(r'the login window should be displayed')
def verify_logout_of_application(context):
    pass


@when(r'I execute the application')
def execute(context):
    context._app.exec_()




