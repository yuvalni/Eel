from tests.utils import get_eel_server


def test_hello_world(driver):
    with get_eel_server('examples/01 - hello_world/hello.py', 'hello.html') as eel_url:
        driver.get(eel_url)
        assert driver.title == "Hello, World!"

        console_logs = driver.get_log('browser')
        assert "Hello from Javascript World!" in console_logs[0]['message']
        assert "Hello from Python World!" in console_logs[1]['message']
