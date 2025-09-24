from src.app import TimeCatchClockApp
from src.test import TestApp

if __name__ == '__main__':
    try:
        TestApp().run()
    except Exception as e:
        import traceback
        with open('error.log', 'w') as f:
            f.write(str(e))
            f.write(traceback.format_exc())
        print("Error occurred, see error.log for details")